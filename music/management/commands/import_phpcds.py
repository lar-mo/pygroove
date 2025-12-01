import json
from django.core.management.base import BaseCommand
from music.models import Genre, RecordLabel, Artist, Album


class Command(BaseCommand):
    help = 'Import data from phpCDs JSON exports'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import...'))
        
        # Import genres first
        self.import_genres()
        
        # Import albums (which creates artists and labels)
        self.import_albums()
        
        self.stdout.write(self.style.SUCCESS('Import completed!'))

    def import_genres(self):
        self.stdout.write('Importing genres...')
        
        with open('genre_desc.json', 'r') as f:
            data = json.load(f)
        
        # Find the data array
        genre_data = None
        for item in data:
            if item.get('type') == 'table' and item.get('name') == 'genre_desc':
                genre_data = item.get('data', [])
                break
        
        if not genre_data:
            self.stdout.write(self.style.ERROR('No genre data found'))
            return
        
        count = 0
        for genre_item in genre_data:
            genre_name = genre_item.get('genreName')
            genre_desc = genre_item.get('genreDesc') or ''
            
            if genre_name:
                genre, created = Genre.objects.get_or_create(
                    name=genre_name,
                    defaults={'description': genre_desc}
                )
                if created:
                    count += 1
                    self.stdout.write(f'  Created genre: {genre_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Imported {count} genres'))

    def import_albums(self):
        self.stdout.write('Importing albums...')
        
        with open('cds.json', 'r') as f:
            data = json.load(f)
        
        # Find the data array
        album_data = None
        for item in data:
            if item.get('type') == 'table' and item.get('name') == 'cds':
                album_data = item.get('data', [])
                break
        
        if not album_data:
            self.stdout.write(self.style.ERROR('No album data found'))
            return
        
        album_count = 0
        artist_count = 0
        label_count = 0
        
        for cd_item in album_data:
            artist_name = cd_item.get('artist')
            album_title = cd_item.get('album')
            genre_name = cd_item.get('genre')
            release_date = cd_item.get('release_date')
            number_of_discs = cd_item.get('number_of_discs', '1')
            label_name = cd_item.get('record_label')
            
            # Get or create Artist
            artist, created = Artist.objects.get_or_create(name=artist_name)
            if created:
                artist_count += 1
                self.stdout.write(f'  Created artist: {artist_name}')
            
            # Get or create RecordLabel
            label = None
            if label_name:
                label, created = RecordLabel.objects.get_or_create(name=label_name)
                if created:
                    label_count += 1
                    self.stdout.write(f'  Created label: {label_name}')
            
            # Get Genre
            genre = None
            if genre_name:
                try:
                    genre = Genre.objects.get(name=genre_name)
                except Genre.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Genre not found: {genre_name}'))
            
            # Parse release date (just store the year for now, as dates are inconsistent)
            release_year = None
            if release_date:
                # Try to extract year from various formats
                import re
                year_match = re.search(r'\d{4}', release_date)
                if year_match:
                    release_year = year_match.group()
            
            # Create Album
            album, created = Album.objects.get_or_create(
                title=album_title,
                artist=artist,
                defaults={
                    'genre': genre,
                    'release_date': f'{release_year}-01-01' if release_year else None,
                    'number_of_discs': int(number_of_discs),
                    'record_label': label,
                }
            )
            
            if created:
                album_count += 1
                self.stdout.write(f'  Created album: {album_title} by {artist_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Imported {album_count} albums, {artist_count} artists, {label_count} labels'))
