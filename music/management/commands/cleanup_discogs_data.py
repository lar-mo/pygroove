import re
from django.core.management.base import BaseCommand
from music.models import Artist

class Command(BaseCommand):
    help = 'Clean up Discogs formatting in artist bios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        artists_with_bios = Artist.objects.exclude(bio='')
        total = artists_with_bios.count()
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f"DRY RUN MODE - No changes will be made"))
        
        self.stdout.write(f"Processing {total} artists with bios...")
        
        updated_count = 0
        
        for i, artist in enumerate(artists_with_bios, 1):
            original_bio = artist.bio
            cleaned_bio = self.clean_discogs_markup(original_bio)
            
            if cleaned_bio != original_bio:
                self.stdout.write(f"[{i}/{total}] {artist.name}")
                
                if not dry_run:
                    artist.bio = cleaned_bio
                    artist.save()
                    updated_count += 1
                else:
                    self.stdout.write(f"  Would clean markup")
                    # Show sample of changes
                    if '[a=' in original_bio or '[url=' in original_bio:
                        self.stdout.write(f"    Before (sample): {original_bio[:100]}...")
                        self.stdout.write(f"    After (sample): {cleaned_bio[:100]}...")
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"\nDRY RUN: Would update {updated_count} artists"))
        else:
            self.stdout.write(self.style.SUCCESS(f"\n✓ Updated {updated_count} artists"))

    def clean_discogs_markup(self, text):
        """
        Clean up Discogs markup from bio text:
        - Remove [a=Artist Name] tags (keep just the artist name)
        - Remove [url=...]text[/url] tags (keep just the text)
        - Remove [aXXXXX] numeric artist IDs
        - Normalize line endings and paragraph breaks
        """
        if not text:
            return text
        
        # Normalize line endings (convert \r\n to \n)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove [a=Artist (id)] - extract artist name without ID
        # Example: [a=King Diamond (2)] -> King Diamond
        text = re.sub(r'\[a=([^\]]+?)\s*\(\d+\)\]', r'\1', text)
        
        # Remove [a=Artist] - keep just the artist name
        # Example: [a=Mercyful Fate] -> Mercyful Fate
        text = re.sub(r'\[a=([^\]]+)\]', r'\1', text)
        
        # Remove [aXXXXX] - numeric artist IDs without names
        # Example: [a151718] -> (removed)
        text = re.sub(r'\[a\d+\]', '', text)
        
        # Remove [url=...]text[/url] - keep just the text
        # Example: [url=https://example.com]Click Here[/url] -> Click Here
        text = re.sub(r'\[url=[^\]]+\]([^\[]+)\[/url\]', r'\1', text)
        
        # Remove [l=Label] - label references
        # Example: [l=Metalheadz] -> Metalheadz
        text = re.sub(r'\[l=([^\]]+)\]', r'\1', text)
        
        # Remove [r=Release ID] - release references
        text = re.sub(r'\[r=?\d*\]', '', text)
        
        # Normalize multiple spaces
        text = re.sub(r'  +', ' ', text)
        
        # Preserve double newlines (paragraph breaks) but normalize to exactly 2
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()
