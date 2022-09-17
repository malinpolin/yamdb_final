import csv
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User
from reviews.models import Comment, Review

comments = os.path.join(settings.CSV_FILES_DIR, "comments.csv")


class Command(BaseCommand):
    help = "Importing a csv file into a database"

    def handle(self, *args, **options):
        with open(comments, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(csv_file, None)
            try:
                for row in reader:
                    try:
                        Comment.objects.create(
                            id=int(row[0]),
                            review=Review.objects.get(id=row[1]),
                            text=row[2],
                            author=User.objects.get(id=int(row[3])),
                            pub_date=row[4],
                        )
                    except Exception as error:
                        if "UNIQUE constraint" in str(error.args):
                            print(
                                f"Error. The row with ID {int(row[0])} "
                                "is already in the database."
                            )
            except csv.Error as error:
                sys.exit(f"File {comments}, line {reader.line_num}: {error}")
