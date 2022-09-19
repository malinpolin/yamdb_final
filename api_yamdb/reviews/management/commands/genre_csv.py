import csv
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Genre

genre = os.path.join(settings.CSV_FILES_DIR, "genre.csv")


class Command(BaseCommand):
    help = "Importing a csv file into a database"

    def handle(self, *args, **options):
        with open(genre, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(csv_file, None)
            try:
                for row in reader:
                    try:
                        Genre.objects.create(
                            id=int(row[0]),
                            name=row[1],
                            slug=row[2]
                        )
                    except Exception as error:
                        if "UNIQUE constraint" in str(error.args):
                            print(
                                f"Error. The row with ID {int(row[0])} "
                                "is already in the database."
                            )
            except csv.Error as error:
                sys.exit(f"File {genre}, line {reader.line_num}: {error}")
