import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт csv файлов в базу данных'

    def handle(self, *args, **kwargs):

        with open(
            f'{settings.CSV_FILE_PATH}', 'r', encoding='utf8'
        ) as file_csv:
            reader = csv.reader(file_csv, delimiter=',')
            Ingredient.objects.bulk_create(
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in list(reader)[1:]
            )
        self.stdout.write(
            f'Файл импортирован в БД {Ingredient}'
        )
