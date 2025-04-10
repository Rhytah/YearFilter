import os
import gzip
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection
from api.models import PageYear

class Command(BaseCommand):
    help = 'Import page-year data from a file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file (can be gzipped)')
        parser.add_argument(
            '--chunk-size',
            type=int,
            default=5000,
            help='Number of records to insert in a batch (default: 5000)'
        )
        parser.add_argument(
            '--keep-existing',
            action='store_true',
            help='Do not clear existing data before import'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        chunk_size = options['chunk_size']
        keep_existing = options['keep_existing']
        
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')
        
        self.stdout.write(f'Importing data from {file_path}...')
        start_time = time.time()
        
        try:
            # Clear existing data if not keeping it
            if not keep_existing:
                self.stdout.write('Clearing existing data...')
                PageYear.objects.all().delete()
                self.stdout.write('Existing data cleared.')
            
            # Determine if the file is gzipped based on extension
            is_gzipped = file_path.endswith('.gz')
            open_func = gzip.open if is_gzipped else open
            mode = 'rt' if is_gzipped else 'r'
            
            # Parse and insert data in chunks
            total_records = 0
            batch = []
            
            with open_func(file_path, mode) as f:
                # Skip header line
                next(f, None)
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse line
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        try:
                            page_id = int(parts[0])
                            year = int(parts[1])
                            batch.append(PageYear(page_id=page_id, year=year))
                            total_records += 1
                        except ValueError:
                            self.stderr.write(f'Warning: Invalid record: {line}')
                            continue
                    
                    # Bulk insert when batch reaches chunk size
                    if len(batch) >= chunk_size:
                        with transaction.atomic():
                            PageYear.objects.bulk_create(
                                batch, 
                                update_conflicts=True,
                                unique_fields=['page_id'],
                                update_fields=['year']
                            )
                        self.stdout.write(f'Imported {total_records} records so far...')
                        batch = []
            
            # Insert any remaining records
            if batch:
                with transaction.atomic():
                    PageYear.objects.bulk_create(
                        batch, 
                        update_conflicts=True,
                        unique_fields=['page_id'],
                        update_fields=['year']
                    )
            
            elapsed_time = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported {total_records} records in {elapsed_time:.2f} seconds.'
                )
            )
            
        except Exception as e:
            raise CommandError(f'Error during import: {str(e)}')

    def _bulk_import_raw_sql(self, batch, keep_existing):
        """
        Alternative method for bulk import using raw SQL.
        This can be faster for very large datasets on some database backends.
        """
        if not batch:
            return
            
        # Create a temporary table for importing
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TEMPORARY TABLE temp_page_years (
                    page_id INTEGER PRIMARY KEY,
                    year SMALLINT
                )
            ''')
            
            # Insert data into temporary table
            placeholders = ', '.join(['(%s, %s)'] * len(batch))
            flat_values = []
            for item in batch:
                flat_values.extend([item.page_id, item.year])
                
            cursor.execute(f'''
                INSERT INTO temp_page_years (page_id, year)
                VALUES {placeholders}
            ''', flat_values)
            
            # Either replace or merge with existing data
            if not keep_existing:
                cursor.execute('''
                    DELETE FROM page_years
                ''')
                
            cursor.execute('''
                INSERT INTO page_years (page_id, year)
                SELECT page_id, year FROM temp_page_years
                ON CONFLICT (page_id) DO UPDATE SET year = EXCLUDED.year
            ''')
            
            # Drop the temporary table
            cursor.execute('''
                DROP TABLE temp_page_years
            ''')
            