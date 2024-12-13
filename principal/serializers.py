from rest_framework import serializers
from .models import Post, Comment
from drf_spectacular.utils import extend_schema_field


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content"]


class PostSerializerResponse(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_username",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.CharField)
    def get_author_username(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ["content", "post"]

    def validate_post(self, value):
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("Post does not exist")
        return value


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["content"]


class CommentSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostWithCommentsSerializerResponse(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_username",
            "created_at",
            "updated_at",
            "comments",
        ]

    @extend_schema_field(serializers.CharField)
    def get_author_username(self, obj):
        return obj.author.username

    @extend_schema_field(serializers.ListField)
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializerResponse(comments, many=True).data
