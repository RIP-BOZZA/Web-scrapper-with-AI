from rest_framework import serializers
from .models import EntitiesMaster,Programs,Artists


class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        exclude =['id']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        exclude =['id']


class EntitiesMasterSerializer(serializers.ModelSerializer):
    programs = ProgramsSerializer(read_only=True,many=True)
    artists = ArtistSerializer(read_only=True,many=True)
    class Meta:
        model = EntitiesMaster
        exclude =['id']