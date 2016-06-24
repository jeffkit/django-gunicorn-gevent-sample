# coding:utf-8
from django.contrib import admin
from . models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['name',]


admin.site.register(Book, BookAdmin)
