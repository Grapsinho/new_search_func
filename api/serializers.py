from rest_framework import serializers
from .models import *

class bookSerializer(serializers.ModelSerializer):
    title_headline = serializers.CharField()
    author_headline = serializers.CharField()
    class Meta:
        model = Book
        fields = ["id", "title", "authors", "title_headline", "author_headline"]