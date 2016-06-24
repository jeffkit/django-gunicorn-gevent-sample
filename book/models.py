# coding:utf-8


from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    name = models.CharField(u'名称', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'书'
        verbose_name_plural = u'书'
