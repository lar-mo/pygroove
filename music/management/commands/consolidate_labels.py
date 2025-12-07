from django.core.management.base import BaseCommand
from music.models import Album, RecordLabel


class Command(BaseCommand):
    help = 'Consolidate duplicate record labels by moving albums from one label to another'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-label-id',
            type=int,
            help='ID of the label to move albums FROM'
        )
        parser.add_argument(
            '--to-label-id',
            type=int,
            help='ID of the label to move albums TO'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all record labels with their IDs and album counts'
        )
        parser.add_argument(
            '--delete-old',
            action='store_true',
            help='Delete the old label after moving albums'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would happen without making changes'
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_labels()
            return

        from_label_id = options.get('from_label_id')
        to_label_id = options.get('to_label_id')

        if not from_label_id or not to_label_id:
            self.stdout.write(self.style.ERROR('Error: --from-label-id and --to-label-id are required'))
            self.stdout.write('Use --list to see all labels and their IDs')
            return

        try:
            from_label = RecordLabel.objects.get(id=from_label_id)
            to_label = RecordLabel.objects.get(id=to_label_id)
        except RecordLabel.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            return

        # Get albums to move
        albums = Album.objects.filter(record_label=from_label)
        count = albums.count()

        if count == 0:
            self.stdout.write(self.style.WARNING(f'No albums found under "{from_label.name}"'))
            return

        self.stdout.write(f'\n{self.style.WARNING("="*70)}')
        self.stdout.write(f'FROM: {from_label.name} (ID: {from_label.id})')
        self.stdout.write(f'TO:   {to_label.name} (ID: {to_label.id})')
        self.stdout.write(f'Albums to move: {count}')
        self.stdout.write(f'{self.style.WARNING("="*70)}\n')

        # Show albums
        self.stdout.write('Albums that will be moved:')
        for album in albums:
            self.stdout.write(f'  • [{album.id}] {album.artist.name} - {album.title}')

        if options['dry_run']:
            self.stdout.write(f'\n{self.style.WARNING("DRY RUN - No changes made")}')
            return

        # Confirm
        self.stdout.write(f'\n{self.style.WARNING("Are you sure you want to proceed? (yes/no)")}')
        confirm = input().lower()

        if confirm != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))
            return

        # Move albums
        updated = albums.update(record_label=to_label)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Moved {updated} albums to "{to_label.name}"'))

        # Delete old label if requested
        if options['delete_old']:
            # Double check it's empty
            remaining = Album.objects.filter(record_label=from_label).count()
            if remaining == 0:
                from_label.delete()
                self.stdout.write(self.style.SUCCESS(f'✓ Deleted old label "{from_label.name}"'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ Cannot delete label - {remaining} albums still associated'))

    def list_labels(self):
        """List all record labels with their IDs and album counts"""
        labels = RecordLabel.objects.all().order_by('name')
        
        self.stdout.write(f'\n{self.style.SUCCESS("="*70)}')
        self.stdout.write(f'{self.style.SUCCESS("All Record Labels")}')
        self.stdout.write(f'{self.style.SUCCESS("="*70)}\n')
        
        for label in labels:
            count = Album.objects.filter(record_label=label).count()
            self.stdout.write(f'[{label.id:3d}] {label.name:40s} ({count} albums)')
        
        self.stdout.write(f'\n{self.style.SUCCESS("="*70)}')
        self.stdout.write(f'Total labels: {labels.count()}\n')
