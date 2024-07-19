from django.db import models


class Artists(models.Model):
    artist_name = models.CharField(max_length=50)
    artist_role = models.CharField(max_length=50)


class Programs(models.Model):
    program_name = models.CharField(max_length=50)
    program_composer = models.CharField(max_length=50,null=True,blank=True)


class EntitiesMaster(models.Model):
    auditorium =models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    date = models.CharField(max_length=60)
    programs = models.ManyToManyField(Programs)
    artists = models.ManyToManyField(Artists)
