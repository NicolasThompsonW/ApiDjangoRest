from principal.serializers import Comment, CommentSerializer, CommentUpdateSerializer, CommentSerializerResponse
from principal.models import User, Post  # Import Post model


def error_formater(errors):
    error_messages = [
        f"{field}: {error[0]}" for field, error in errors.items()]
    return f"Invalid data: {', '.join(error_messages)}"


class CommentRepository:
    @staticmethod
    def create_comment(comment_serializer: CommentSerializer, user: User):
        if not comment_serializer.is_valid():
            error_messages = error_formater(comment_serializer.errors)
            raise ValueError(f"Invalid comment data: {error_messages}")
        post = comment_serializer.validated_data["post"]
        content = comment_serializer.validated_data["content"]
        comment = Comment.objects.create(
            author=user, post=post, content=content)
        return comment

    @staticmethod
    def update_comment(pk: int, request, update_data: CommentUpdateSerializer):
        if update_data.is_valid():
            try:
                comment = Comment.objects.get(id=pk)
                if comment is not None:
                    if comment.author == request.user:
                        comment.content = update_data.validated_data["content"]
                        comment.save()
                        return comment
                    else:
                        raise ValueError("You can't update this comment")
                else:
                    raise ValueError("Comment not found")
            except Exception as e:
                raise ValueError(str(e))

    @staticmethod
    def comment_delete(pk: int, request):
        try:
            comment = Comment.objects.get(id=pk)
            if comment.author == request.user:
                comment.delete()
            else:
                raise ValueError("You can't delete this comment")
        except Exception as e:
            raise ValueError(str(e))
