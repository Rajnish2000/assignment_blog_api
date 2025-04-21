"""
Serializers for the blog API.
"""
from rest_framework import serializers
from core.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """ Serializer for blog post objects """

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'is_published']
        read_only_fields = ['id']


class BlogPostDetailSerializer(BlogPostSerializer):
    """ Serializer for blog post detail """

    class Meta(BlogPostSerializer.Meta):
        fields = BlogPostSerializer.Meta.fields + ['created_at', 'updated_at']
