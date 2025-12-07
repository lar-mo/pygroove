import discogs_client
import requests
import time
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from music.models import Album, Artist, Genre, RecordLabel, Track

class Command(BaseCommand):
    help = 'Import or update album data from Discogs API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--album-id',
            type=int,
            help='Specific album ID to update'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all albums in database'
        )
        parser.add_argument(
            '--missing-only',
            action='store_true',
            help='Only update albums missing cover images or tracks'
        )

    def handle(self, *args, **options):
        # Initialize Discogs client
        d = discogs_client.Client(
            'PyGroove/1.0',
            user_token=settings.DISCOGS_TOKEN
        )

        if options['album_id']:
            # Update single album
            try:
                album = Album.objects.get(id=options['album_id'])
                self.update_album_from_discogs(album, d)
            except Album.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Album with ID {options['album_id']} not found"))
        
        elif options['all']:
            # Update all albums
            albums = Album.objects.all()
            total = albums.count()
            self.stdout.write(f"Updating {total} albums from Discogs...")
            
            for i, album in enumerate(albums, 1):
                self.stdout.write(f"[{i}/{total}] Processing: {album.artist.name} - {album.title}")
                self.update_album_from_discogs(album, d)
                time.sleep(1.5)  # Rate limit: ~40 requests/min (well under 60/min limit)
        
        elif options['missing_only']:
            # Update albums without covers or tracks
            from django.db.models import Q
            albums = Album.objects.filter(Q(cover_image='') | Q(tracks__isnull=True)).distinct()
            total = albums.count()
            self.stdout.write(f"Updating {total} albums missing data...")
            
            for i, album in enumerate(albums, 1):
                self.stdout.write(f"[{i}/{total}] Processing: {album.artist.name} - {album.title}")
                self.update_album_from_discogs(album, d)
                time.sleep(1.5)  # Rate limit: ~40 requests/min (well under 60/min limit)
        
        else:
            self.stdout.write(self.style.WARNING("Please specify --album-id, --all, or --missing-only"))

    def update_album_from_discogs(self, album, discogs_client):
        """Search Discogs and update album data"""
        try:
            # Search for the album - prefer master release for canonical tracklist
            query = f"{album.artist.name} {album.title}"
            
            # First try to find master release (canonical version)
            master_results = discogs_client.search(query, type='master')
            
            if master_results:
                # Get the main release from the master
                master = master_results[0]
                release = master.main_release
                self.stdout.write(self.style.SUCCESS(f"  → Found master release"))
            else:
                # Fall back to regular release search
                release_results = discogs_client.search(query, type='release')
                if not release_results:
                    self.stdout.write(self.style.WARNING(f"  No results found for: {query}"))
                    return
                release = release_results[0]
                self.stdout.write(self.style.WARNING(f"  → Using specific release (no master found)"))
            
            # Download and save cover image
            if release.images and not album.cover_image:
                self.download_cover_image(album, release.images[0]['uri'])
            
            # Update tracklist
            if hasattr(release, 'tracklist') and release.tracklist:
                self.update_tracklist(album, release.tracklist)
            
            # Update artist info if available
            if hasattr(release, 'artists') and release.artists:
                self.update_artist_info(album.artist, release.artists[0], discogs_client)
            
            # Update other metadata
            if hasattr(release, 'genres') and release.genres:
                self.update_genre(album, release.genres[0])
            
            if hasattr(release, 'labels') and release.labels:
                self.update_label(album, release.labels[0].name)
            
            if hasattr(release, 'year') and release.year:
                if not album.release_date:
                    album.release_date = f"{release.year}-01-01"
            
            album.save()
            self.stdout.write(self.style.SUCCESS(f"  ✓ Updated: {album.title}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Error updating {album.title}: {str(e)}"))

    def download_cover_image(self, album, image_url):
        """Download and save album cover image"""
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                filename = f"{album.artist.name}_{album.title}.jpg".replace(' ', '_').replace('/', '_')
                album.cover_image.save(filename, File(img_temp), save=True)
                self.stdout.write(self.style.SUCCESS(f"    → Cover image downloaded"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"    → Could not download image: {str(e)}"))

    def update_tracklist(self, album, tracklist):
        """Update album tracks"""
        try:
            # Delete existing tracks
            album.tracks.all().delete()
            
            # Add new tracks
            track_counter = 1
            for track_data in tracklist:
                position = track_data.position
                title = track_data.title
                duration = track_data.duration if hasattr(track_data, 'duration') else ''
                
                # Convert position to track number
                # Handle formats like "1", "A1", "B2", "1-1", etc.
                track_number = 0
                try:
                    if position.isdigit():
                        # Simple numeric position like "1", "2"
                        track_number = int(position)
                    else:
                        # Extract numbers from positions like "A1", "B2", "1-1"
                        # Just use sequential numbering for vinyl sides
                        import re
                        numbers = re.findall(r'\d+', position)
                        if numbers:
                            track_number = track_counter
                            track_counter += 1
                        else:
                            # No numbers found, use sequential
                            track_number = track_counter
                            track_counter += 1
                except (ValueError, AttributeError):
                    track_number = track_counter
                    track_counter += 1
                
                if track_number > 0:  # Only add tracks with valid numbers
                    Track.objects.create(
                        album=album,
                        title=title,
                        track_number=track_number,
                        duration=duration
                    )
            
            tracks_added = album.tracks.count()
            self.stdout.write(self.style.SUCCESS(f"    → Added {tracks_added} tracks"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"    → Could not update tracks: {str(e)}"))

    def update_artist_info(self, artist, discogs_artist, discogs_client):
        """Update artist bio and image"""
        try:
            # Fetch full artist data
            artist_data = discogs_client.artist(discogs_artist.id)
            
            # Update bio if available
            if hasattr(artist_data, 'profile') and artist_data.profile and not artist.bio:
                artist.bio = artist_data.profile
                self.stdout.write(self.style.SUCCESS(f"    → Updated artist bio"))
            
            # Download artist image if available
            if hasattr(artist_data, 'images') and artist_data.images and not artist.image:
                image_url = artist_data.images[0]['uri']
                response = requests.get(image_url)
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()
                    
                    filename = f"{artist.name}.jpg".replace(' ', '_').replace('/', '_')
                    artist.image.save(filename, File(img_temp), save=True)
                    self.stdout.write(self.style.SUCCESS(f"    → Downloaded artist image"))
            
            artist.save()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"    → Could not update artist: {str(e)}"))

    def update_genre(self, album, genre_name):
        """Update or create genre"""
        try:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            album.genre = genre
            if created:
                self.stdout.write(self.style.SUCCESS(f"    → Created genre: {genre_name}"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"    → Could not update genre: {str(e)}"))

    def update_label(self, album, label_name):
        """Update or create record label"""
        try:
            label, created = RecordLabel.objects.get_or_create(name=label_name)
            album.record_label = label
            if created:
                self.stdout.write(self.style.SUCCESS(f"    → Created label: {label_name}"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"    → Could not update label: {str(e)}"))
