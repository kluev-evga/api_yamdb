# api_yamdb

[![python version](https://img.shields.io/static/v1?label=Python&message=3.11.2&color=97ca00&style=for-the-badge)](https://python.org)
[![django version](https://img.shields.io/static/v1?label=DJANGO&message=3.2.0&color=97ca00&style=for-the-badge)](https://www.djangoproject.com/)
[![drf version](https://img.shields.io/static/v1?label=DRF&message=3.12.4&color=97ca00&style=for-the-badge)](https://www.django-rest-framework.org/)
![api version](https://img.shields.io/static/v1?label=API%20VERSION&message=1.0.0&color=97ca00&style=for-the-badge)
[![licence](https://img.shields.io/static/v1?label=LICENSE&message=MIT&color=97ca00&style=for-the-badge)](https://github.com/kluevEVGA/api_final_yatube/blob/master/LICENSE)

## О ПРОЕКТЕ

Проект реализует REST API backend сервис на базе встроенной в Python sqlite базы данных и django reset framework. В
проекте подключена авторизация по JWT токенам.

## Установка

Клонировать проект

```shell
git clone https://github.com/kluevEVGA/api_yamdb.git
```

Установка окружения

```shell
python3 -m venv env
```

```shell
py -m venv venv
```

Активировать окружение

```shell
.\venv\Scripts\activate
```

```shell
source env/bin/activate
```

Установка зависимостей

```shell
pip install -r requirements.txt
```

## Запуск сервера

Перейти в папку с проектом

```shell
cd .\api_yamdb\
```

Выполнить миграции

```shell
python3 manage.py migrate
```

запустить сервер

```shell
python3 manage.py runserver
```

## БАЗА ДАННЫХ

База данных построена на основе SQLITE.  
[Схема](https://dbdocs.io/kluev.evga/yamdb?schema=public&view=relationships&table=genre_title) базы данных создана при
помощи [DBML](https://www.dbml.org/docs/#project-definition) синтаксиса и приложения [dbdocs](https://dbdocs.io/).  
Файл схеммы [graph-db.dbml](https://github.com/kluevEVGA/api_yamdb/blob/master/graph-db.dbml).

[Установка](https://dbdocs.io/docs) и запуск приложения dbdocs:

```shell
npm install -g dbdocs
```

```shell
dbdocs login
```

выбрать метод аутентификации Email, скопировать код из email и вставить в консоль

```shell
dbdocs build graph-db.dbml
```

Последний шаг выведет в консоль ссылку на задеплоенный проект.

## ЛИЦЕНЗИЯ

Распространяется по `MIT` лицензии. Для дополнительной информации
смотри: [LICENSE](https://github.com/kluevEVGA/api_yamdb/blob/master/LICENSE)