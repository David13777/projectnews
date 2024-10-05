from rest_framework import serializers
from news.models import Author, Post


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['user', 'rating']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['author', 'post_type', 'date_in', 'category', 'title', 'text', 'rating']