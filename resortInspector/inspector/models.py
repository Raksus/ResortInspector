from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Itemsequiped(models.Model):
    idplayer = models.IntegerField(blank=True, null=True)
    iditem = models.IntegerField(blank=True, null=True)
    context = models.CharField(max_length=20, blank=True, null=True)
    bonuslist = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    part = models.CharField(max_length=15, blank=True, null=True)
    ilvl = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemsequiped'

    def __str__(self):
        return self.name
@python_2_unicode_compatible
class Itemshistoric(models.Model):
    idplayer = models.IntegerField(blank=True, null=True)
    iditem = models.IntegerField(blank=True, null=True)
    context = models.CharField(max_length=20, blank=True, null=True)
    bonuslist = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    part = models.CharField(max_length=15, blank=True, null=True)
    ilvl = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemshistoric'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Players(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    realm = models.CharField(max_length=20, blank=True, null=True)
    ilvl = models.IntegerField(blank=True, null=True)
    class_field = models.IntegerField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    race = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    lvl = models.IntegerField(blank=True, null=True)
    faction = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'

    def __str__(self):
        return self.name
