# coding:utf-8
from django.http import HttpResponse
from . models import Book
import random
import requests


def random_search(request):
    books = [book for book in Book.objects.all()]
    random.shuffle(books)
    url = 'https://www.baidu.com/s?wd=' + books[0].name
    rsp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'})
    print rsp.status_code
    return HttpResponse(rsp.text)
