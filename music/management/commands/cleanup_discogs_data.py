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
        - Add paragraph breaks for double newlines
        """
        if not text:
            return text
        
        # Remove [a=Artist (id)] - extract artist name without ID
        # Example: [a=King Diamond (2)] -> King Diamond
        text = re.sub(r'\[a=([^\]]+?)\s*\(\d+\)\]', r'\1', text)
        
        # Remove [a=Artist] - keep just the artist name
        # Example: [a=Mercyful Fate] -> Mercyful Fate
        text = re.sub(r'\[a=([^\]]+)\]', r'\1', text)
        
        # Remove [url=...]text[/url] - keep just the text
        # Example: [url=https://example.com]Click Here[/url] -> Click Here
        text = re.sub(r'\[url=[^\]]+\]([^\[]+)\[/url\]', r'\1', text)
        
        # Convert double newlines to paragraph breaks
        # This helps with readability
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()
