import json
import os
from django.core.management.base import BaseCommand
from music.models import Album


class Command(BaseCommand):
    help = 'Link album cover images to albums based on phpCDs ID'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Linking album cover images...'))
        
        # Load the phpCDs data to get ID mappings
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
        
        updated_count = 0
        missing_count = 0
        
        for cd_item in album_data:
            phpcds_id = cd_item.get('id')
            artist_name = cd_item.get('artist')
            album_title = cd_item.get('album')
            
            # Find the album in our database
            try:
                album = Album.objects.get(title=album_title, artist__name=artist_name)
                
                # Check if cover image exists
                cover_filename = f'album_covers/cover{phpcds_id}.jpg'
                cover_path = os.path.join('media', cover_filename)
                
                if os.path.exists(cover_path):
                    album.cover_image = cover_filename
                    album.save()
                    updated_count += 1
                    self.stdout.write(f'  Linked cover for: {album_title}')
                else:
                    missing_count += 1
                    self.stdout.write(self.style.WARNING(f'  No image file for: {album_title} (cover{phpcds_id}.jpg)'))
                    
            except Album.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Album not found: {album_title} by {artist_name}'))
            except Album.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'  Multiple albums found: {album_title} by {artist_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Linked {updated_count} album covers'))
        self.stdout.write(self.style.WARNING(f'{missing_count} images not found'))
