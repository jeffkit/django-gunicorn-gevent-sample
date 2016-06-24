# coding:utf-8
from __future__ import unicode_literals
from django.db.models.signals import post_migrate
from django.db import DEFAULT_DB_ALIAS, router
from django.apps import AppConfig, apps


def create_default_books(app_config, verbosity=2, interactive=True,
                         using=DEFAULT_DB_ALIAS, **kwargs):
    try:
        Book = apps.get_model('book', 'Book')
    except LookupError:
        if verbosity >= 2:
            print 'Lookup Error'
        return

    if not router.allow_migrate_model(using, Book):
        if verbosity >= 2:
            print 'not allow migrate'
        return

    if Book.objects.using(using).exists():
        if verbosity >= 2:
            print 'books exists'
        return

    books = ['python', 'java', 'ruby', 'haskell', 'lisp', '.net', 'scala',
             'golang', 'schema', 'rocket', 'clojure']
    Book.objects.bulk_create(
        [Book(name=b) for b in books])

    if verbosity >= 2:
        print 'books created'


class BookConfig(AppConfig):
    name = 'book'
    verbose_name = u'书'

    def ready(self):
        post_migrate.connect(create_default_books, sender=self)
