from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    """
    PostSerializer is a serializer for the Post model, providing serialization and deserialization
    of Post instances, as well as custom handling for related fields and additional functionality.
    Fields:
        - id (int): The unique identifier of the post (read-only).
        - author (str): The username of the post's author (read-only).
        - title (str): The title of the post.
        - content (str): The content of the post.
        - category (str): The category of the post.
        - tags (list): A list of tags associated with the post.
        - created_at (datetime): The timestamp when the post was created (read-only).
        - updated_at (datetime): The timestamp when the post was last updated (read-only).
        - likes_count (int): The number of likes the post has received (read-only).
    Methods:
        - get_likes_count(obj): Returns the number of likes for the given post instance.
        - create(validated_data): Creates a new Post instance with the provided validated data,
          associates tags if provided, and sets the author to the current user.
        - update(instance, validated_data): Updates an existing Post instance with the provided
          validated data, and updates the associated tags if provided.
    """
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'category', 'tags', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes_count
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(author=self.context['request'].user, **validated_data)
        if tags_data:
            post.tags.set(tags_data)
        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags_data is not None:
            instance.tags.set(tags_data)
        return instance
    
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'post', 'author', 'author_username', 'created_at', 'updated_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes_count