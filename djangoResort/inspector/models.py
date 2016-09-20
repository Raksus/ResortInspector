from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Item(models.Model):
    idItem = models.IntegerField()
    name = models.CharField(max_length=100)
    context = models.CharField(max_length=20)
    bonusList = models.CharField(max_length=50, blank=True)
    ITEM_SOCKET = (
        (0, 'Head'),
        (1, 'Neck'),
        (2, 'Shoulder'),
        (3, 'Back'),
        (4, 'Chest'),
        (5, 'Tabard'),
        (6, 'Wrist'),
        (7, 'Hands'),
        (8, 'Waist'),
        (9, 'Legs'),
        (10, 'Feet'),
        (11, 'Finger1'),
        (12, 'Finger2'),
        (13, 'Trinket1'),
        (14, 'Trinket2'),
        (15, 'MainHand'),
        (16, 'OffHand'),
        (17, 'shirt'),
    )
    itemSocket = models.IntegerField(choices=ITEM_SOCKET)

    def __str__(self):
        return str(self.idItem) +", " + str(self.name)

@python_2_unicode_compatible
class ItemStats(models.Model):
    idItem = models.ForeignKey('Item', on_delete=models.CASCADE)
    stat = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.idItem

@python_2_unicode_compatible
class PlayerItem(models.Model):
    idPlayer = models.ForeignKey('Player', on_delete=models.CASCADE)
    idItem = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.idPlayer) + ", " + str(self.idItem)

@python_2_unicode_compatible
class PlayerItemHistoric(models.Model):
    idPlayer = models.ForeignKey('Player', on_delete=models.CASCADE)
    idItem = models.ForeignKey('Item', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idPlayer) + ", " + str(self.idItem) + " (" + str(self.fecha) + ")"

@python_2_unicode_compatible
class Player(models.Model):
    name = models.CharField(max_length=50)
    realm = models.CharField(max_length=20)
    ilvl = models.IntegerField()
    CLASE = (
        ('1', 'Guerrero'),
        ('2', 'Paladin'),
        ('3', 'Cazador'),
        ('4', 'Picaro'),
        ('5', 'Sacerdote'),
        ('6', 'Caballero de la Muerte'),
        ('7', 'Chaman'),
        ('8', 'Mago'),
        ('9', 'Brujo'),
        ('10', 'Monje'),
        ('11', 'Druida'),
        ('12', 'Cazador de demonios'),
    )
    clase = models.IntegerField(choices=CLASE)
    RACE = (
        ('1', 'Humano'),
        ('2', 'Orco'),
        ('3', 'Enano'),
        ('4', 'Elfo de la Noche'),
        ('5', 'NoMuerto'),
        ('6', 'Tauren'),
        ('7', 'Gnomo'),
        ('8', 'Troll'),
        ('9', 'Goblin'),
        ('10', 'Elfo de Sangre'),
        ('11', 'Draenei'),
        ('22', 'Worgen'),
        ('24', 'Pandaren'),
        ('25', 'Pandaren'),
        ('26', 'Pandaren'),
    )
    race = models.IntegerField(choices=RACE)
    GENDER = (
        ('0', 'M'),
        ('1', 'F'),
    )
    gender = models.IntegerField(choices=GENDER)
    lvl = models.IntegerField()
    FACTION = (
        ('0', 'Alianza'),
        ('1', 'Horda'),
    )
    faction = models.IntegerField(choices=FACTION)
    image = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
