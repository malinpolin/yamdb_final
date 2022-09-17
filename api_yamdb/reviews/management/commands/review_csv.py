import csv
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User
from reviews.models import Review, Title

review = os.path.join(settings.CSV_FILES_DIR, "review.csv")


class Command(BaseCommand):
    help = "Importing a csv file into a database"

    def handle(self, *args, **options):
        with open(review, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(csv_file, None)
            try:
                for row in reader:
                    try:
                        Review.objects.create(
                            id=int(row[0]),
                            title=Title.objects.get(id=row[1]),
                            text=row[2],
                            author=User.objects.get(id=int(row[3])),
                            score=int(row[4]),
                            pub_date=row[5],
                        )
                    except Exception as error:
                        if "UNIQUE constraint" in str(error.args):
                            print(
                                f"Error. The row with ID {int(row[0])} "
                                "is already in the database."
                            )
            except csv.Error as error:
                sys.exit(f"File {review}, line {reader.line_num}: {error}")
