# import csv
# import sys
# import sqlite3
# from pathlib import Path
# import os
#
#
# APP_NAME = Path(os.path.dirname(__file__)).name
#
#
# def make_connection_with_db(path_to_db):
#     try:
#         return sqlite3.connect(path_to_db)
#     except sqlite3.Error as err:
#         raise f'Bad connection to {path_to_db}, {err}'
#
#
# def get_cursor_for_db(connector):
#     try:
#         return connector.cursor()
#     except sqlite3.Error as err:
#         raise f'Can not make cursor to {connector}, {err}'
#
#
# def upload_table(path, table_name):
#
#     connector = make_connection_with_db('../db.sqlite3')
#     cursor = get_cursor_for_db(connector)
#
#     with open(path, 'r', newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',')
#         try:
#             for row in reader:
#                 if reader.line_num == 1:
#                     column_names = ','.join(row)
#                 else:
#                     row = ['NULL' if val == ' ' or '' else val for val in row]
#                     data = "'" + "','".join(str(item) for item in row) + "'"
#                     data = data.replace("'NULL'", 'NULL')
#                     print(f'INSERT INTO {table_name}({column_names}) '
#                                    f'VALUES ({data})')
#         except csv.Error as err:
#             sys.exit(f'file {path}, line {reader.line_num}: {err}')
#     connector.commit()
#     connector.close()
#
#
# if __name__ == '__main__':
#     upload_table('../static/data/review.csv', 'reviews_reviews')
kwargs = {"key": 1}
for key in kwargs.keys():
    print(key)
