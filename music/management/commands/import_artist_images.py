import discogs_client
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from music.models import Artist
import time

class Command(BaseCommand):
    help = 'Import artist images from Discogs API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--missing-only',
            action='store_true',
            help='Only import for artists without images'
        )

    def handle(self, *args, **options):
        # Initialize Discogs client
        d = discogs_client.Client(
            'PyGroove/1.0',
            user_token=settings.DISCOGS_TOKEN
        )

        if options['missing_only']:
            artists = Artist.objects.filter(image='')
        else:
            artists = Artist.objects.all()
        
        total = artists.count()
        self.stdout.write(f"Importing images for {total} artists...")
        
        success_count = 0
        fail_count = 0
        
        for i, artist in enumerate(artists, 1):
            self.stdout.write(f"[{i}/{total}] {artist.name}")
            
            try:
                # Search for artist
                results = d.search(artist.name, type='artist')
                
                if not results:
                    self.stdout.write(self.style.WARNING(f"  No results found"))
                    fail_count += 1
                    continue
                
                # Get first result
                artist_data = results[0]
                
                # Download image if available
                if hasattr(artist_data, 'images') and artist_data.images:
                    image_url = artist_data.images[0]['uri']
                    self.stdout.write(f"  Found image: {image_url[:50]}...")
                    
                    # Add headers to avoid 403 Forbidden
                    headers = {
                        'User-Agent': 'PyGroove/1.0',
                        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    }
                    response = requests.get(image_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(response.content)
                        img_temp.flush()
                        
                        filename = f"{artist.name}.jpg".replace(' ', '_').replace('/', '_')
                        artist.image.save(filename, File(img_temp), save=True)
                        self.stdout.write(self.style.SUCCESS(f"  ✓ Downloaded image"))
                        success_count += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"  HTTP {response.status_code}"))
                        fail_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f"  No images available"))
                    fail_count += 1
                
                # Rate limiting
                time.sleep(1.5)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error: {str(e)}"))
                fail_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Success: {success_count}"))
        self.stdout.write(self.style.WARNING(f"✗ Failed: {fail_count}"))
