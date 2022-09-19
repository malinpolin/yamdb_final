import csv
import os
import sys

from accounts.models import User
from django.conf import settings
from django.core.management.base import BaseCommand

users = os.path.join(settings.CSV_FILES_DIR, "users.csv")


class Command(BaseCommand):
    help = "Importing a csv file into a database"

    def handle(self, *args, **options):
        with open(users, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(csv_file, None)
            try:
                for row in reader:
                    try:
                        User.objects.create(
                            id=int(row[0]),
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6],
                        )
                    except Exception as error:
                        if "UNIQUE constraint" in str(error.args):
                            print(
                                f"Error. The row with ID {int(row[0])} "
                                "is already in the database."
                            )
            except csv.Error as error:
                sys.exit(f"File {users}, line {reader.line_num}: {error}")
