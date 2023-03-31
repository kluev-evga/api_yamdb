import csv

from django.core.management.base import BaseCommand

from reviews.forms import CategoriesForm, CommentsForm, GenresForm, GenreTitleForm, ReviewsForm, TitlesForm, UserForm


FILENAME_MODEL_DICT = {
    'category': CategoriesForm,
    'comments': CommentsForm,
    'genre': GenresForm,
    'genre_title': GenreTitleForm,
    'review': ReviewsForm,
    'titles': TitlesForm,
    'users': UserForm,
}


class Command(BaseCommand):
    help = ('imports data from a local csv file. '
            'Expects files named category.csv, comments.csv, '
            'genre.csv, genre_title.csv, review.csv, titles.csv, users.csv')

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)

    def handle(self, *args, **kwargs):
        self.filename = kwargs['file_path'][0].split('.')[0]
        self.file_path = 'static/data/' + kwargs['file_path'][0]
        self.prepare()
        self.main()
        self.finalise()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0

    def main(self):
        self.stdout.write('Starting import')

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
                                      f'Errors while import {self.file_path} | '
                                      f'{row}:\n'
                                      )
                    self.stderr.write(f'{form.errors.as_data()}\n')

    def finalise(self):
        self.stdout.write('Import ends\n'
                          f'Instances imported: {self.imported_counter}\n'
                          f'Instances skipped: {self.skipped_counter}')
