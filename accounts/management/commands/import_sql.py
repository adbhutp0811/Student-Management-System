from django.core.management.base import BaseCommand
from django.db import connection
import re


class Command(BaseCommand):
    help = 'Import data from database.sql into PostgreSQL'

    def handle(self, *args, **options):
        import os
        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'database.sql'
        )
        if not os.path.exists(sql_path):
            self.stdout.write('database.sql not found, skipping.')
            return

        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()

        insert_pattern = re.compile(r'(INSERT INTO\s+"\w+".*?);', re.DOTALL)
        inserts = insert_pattern.findall(content)

        if not inserts:
            self.stdout.write('No INSERT statements found.')
            return

        count = 0
        skipped = 0
        with connection.cursor() as cursor:
            for stmt in inserts:
                table = re.search(r'INSERT INTO\s+"(\w+)"', stmt).group(1)
                if table == 'django_migrations':
                    skipped += 1
                    continue
                try:
                    cursor.execute(stmt)
                    count += 1
                except Exception:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Imported {count} rows ({skipped} skipped) from database.sql'
        ))
