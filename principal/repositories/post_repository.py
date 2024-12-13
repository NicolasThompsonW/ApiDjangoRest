from principal.models import Post
from principal.serializers import PostSerializer
from principal.models import User


class PostRepository:
    @staticmethod
    def create_post(post_serializer: PostSerializer, user: User):
        if post_serializer.is_valid():
            title = post_serializer.validated_data["title"]
            content = post_serializer.validated_data["content"]
            try:
                post = Post.objects.create(
                    title=title, content=content, author=user)
                return post
            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError("Invalid data")

    @staticmethod
    def update_post(post: Post, update_data: PostSerializer):
        if update_data.is_valid():
            try:
                post.title = update_data.validated_data["title"]
                post.content = update_data.validated_data["content"]
                post.save()
                return post
            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError("Invalid data")
