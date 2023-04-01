import csv

from django.core.management.base import BaseCommand

from reviews.forms import (CategoriesForm,
                           CommentsForm,
                           GenreTitleForm,
                           GenresForm,
                           ReviewsForm,
                           TitlesForm,
                           UserForm)


FILENAME_MODEL_DICT = {
    'users.csv': UserForm,
    'category.csv': CategoriesForm,
    'genre.csv': GenresForm,
    'titles.csv': TitlesForm,
    'genre_title.csv': GenreTitleForm,
    'review.csv': ReviewsForm,
    'comments.csv': CommentsForm,
}
DATA_PATH = 'static/data/'


class Command(BaseCommand):
    help = ('imports data from a local csv file. '
            'Expects files named category.csv, comments.csv, '
            'genre.csv, genre_title.csv, review.csv, titles.csv, users.csv')

    def add_arguments(self, parser):
        parser.add_argument('--category.csv',
                            action='store_true',
                            help='Import category.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--comments.csv',
                            action='store_true',
                            help='Import comments.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--genre.csv',
                            action='store_true',
                            help='Import genre.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--genre_title.csv',
                            action='store_true',
                            help='Import genre_title.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--review.csv',
                            action='store_true',
                            help='Import review.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--titles.csv',
                            action='store_true',
                            help='Import titles.csv file in database '
                                 'if it contains valid ids and data')
        parser.add_argument('--users.csv',
                            action='store_true',
                            help='Import users.csv file in database '
                                 'if it contains valid ids and data')

    def _choice_of_particular(self, **kwargs):
        for keys in FILENAME_MODEL_DICT.keys():
            if kwargs[keys]:
                self.filename = keys
                return True
        return False

    def handle(self, *args, **kwargs):
        if self._choice_of_particular(**kwargs):
            self.prepare()
            self.file_path = DATA_PATH + self.filename
            self.main_for_particular()
            self.finalise()

        else:
            for keys, values in FILENAME_MODEL_DICT.items():
                self.prepare()
                self.filename = keys
                self.file_path = DATA_PATH + self.filename
                self.main_for_particular()
                self.finalise()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0

    def _import_csv(self):
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                form = FILENAME_MODEL_DICT[self.filename](data=row)
                if form.is_valid():
                    form.save()
                    self.imported_counter += 1
                else:
                    self.skipped_counter += 1
                    self.stderr.write('-------------------------------------\n'
                                      f'Errors while import {self.file_path} |'
                                      f' {row}:\n'
                                      )
                    self.stderr.write(f'{form.errors.as_data()}\n')

    def main_for_particular(self):
        self.stdout.write('------------------------------------'
                          '------------------------------------\n'
                          f'Starting import {self.filename}')
        self._import_csv()

    def finalise(self):
        self.stdout.write(f'Import {self.filename} ends\n'
                          f'Instances imported: {self.imported_counter}\n'
                          f'Instances skipped: {self.skipped_counter}\n')
