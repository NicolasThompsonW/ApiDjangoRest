from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostSerializerResponse(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_username', 'created_at', 'updated_at']

    def get_author_username(self, obj):
        return obj.author.username

    
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'content'
        
class CommentSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostWithCommentsSerializerResponse(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_username', 'created_at', 'updated_at', 'comments']

    def get_author_username(self, obj):
        return obj.author.username

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializerResponse(comments, many=True).data