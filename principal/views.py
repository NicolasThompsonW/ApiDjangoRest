# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .models import Post, Comment
from drf_spectacular.utils import extend_schema, OpenApiExample,OpenApiResponse
from .serializers import PostSerializer,PostSerializerResponse, CommentSerializer, CommentSerializerResponse, PostWithCommentsSerializerResponse

    
class PostGetAllView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Get all posts",
        responses={
            200: OpenApiResponse(
                description="Posts retrieved successfully",
                response=PostSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value=[
                            {
                                "id":"1",
                                "title": "Post title",
                                "content": "Post content",
                                "author": "user123",
                                "created_at": "2021-07-16T15:00:00",
                                "updated_at": "2021-07-16T15:00:00"
                            }
                        ]
                    )
                ]
            )
        },
    )

    def get(self, request):
        posts = Post.objects.all()
        response_serializer = PostSerializerResponse(posts, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    


class NewPostView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Create a post",
        request=PostSerializer,
        responses={
            201: OpenApiResponse(
                description="Post created successfully",
                response=PostSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "id":"1",
                            "title": "Post title",
                            "content": "Post content",
                            "author": "user123",
                            "created_at": "2021-07-16T15:00:00",
                            "updated_at": "2021-07-16T15:00:00"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "title": [
                                "This field is required."
                            ],
                            "content": [
                                "This field is required."
                            ]
                        }
                    )
                ]
            ) 
        },
    )

    def post(self, request):
        data_serializer = PostSerializer(data=request.data)
        if data_serializer.is_valid():
            post = Post.objects.create(
                title=data_serializer.validated_data["title"],
                content=data_serializer.validated_data["content"],
                author=request.user  
            )
            response_serializer = PostSerializerResponse(post)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Update a post",
        request=PostSerializer,
        responses={
            200: OpenApiResponse(
                description="Post updated successfully",
                response=PostSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "id":"1",
                            "title": "Post title",
                            "content": "Post content",
                            "author": "user123",
                            "created_at": "2021-07-16T15:00:00",
                            "updated_at": "2021-07-16T15:00:00"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "title": [
                                "This field is required."
                            ],
                            "content": [
                                "This field is required."
                            ]
                        }
                    )
                ]
            ) 
        },
    )

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            data_serializer = PostSerializer(data=request.data)
            if data_serializer.is_valid():
                post.title = data_serializer.validated_data["title"]
                post.content = data_serializer.validated_data["content"]
                post.save()
                response_serializer = PostSerializerResponse(post)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not the owner of this post'}, status=status.HTTP_403_FORBIDDEN)


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Delete a post",
        responses={
            204: OpenApiResponse(
                description="Post deleted successfully"
            ),
            403: OpenApiResponse(
                description="Forbidden",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "message": "You are not the owner of this post"
                        }
                    )
                ]
            ) 
        },
    )

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You are not the owner of this post'}, status=status.HTTP_403_FORBIDDEN)

class GetPostView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Get a post",
        responses={
            200: OpenApiResponse(
                description="Post retrieved successfully",
                response=PostWithCommentsSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "id": "1",
                            "title": "Post title",
                            "content": "Post content",
                            "author_username": "user123",
                            "created_at": "2021-07-16T15:00:00",
                            "updated_at": "2021-07-16T15:00:00",
                            "comments": [
                                {
                                    "id": "1",
                                    "content": "Comment content",
                                    "author": "commenter123",
                                    "post": 1,
                                    "created_at": "2021-07-16T15:30:00",
                                    "updated_at": "2021-07-16T15:30:00"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Post not found",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "message": "Post not found"
                        }
                    )
                ]
            ) 
        },
    )

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            response_serializer = PostWithCommentsSerializerResponse(post)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Create a comment",
        request=CommentSerializer,
        responses={
            201: OpenApiResponse(
                description="Comment created successfully",
                response=CommentSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "content": "Comment content",
                            "post": 1
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "content": [
                                "This field is required."
                            ]
                        }
                    )
                ]
            ) 
        },
    )

    def post(self, request):
        data_serializer = CommentSerializer(data=request.data)
        if data_serializer.is_valid():
            comment = Comment.objects.create(
                content=data_serializer.validated_data["content"],
                post_id=data_serializer.validated_data["post"],
                author=request.user
            )
            response_serializer = CommentSerializerResponse(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Update a comment",
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(
                description="Comment updated successfully",
                response=CommentSerializerResponse,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "content": "Comment content",
                            "post": 1
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "content": [
                                "This field is required."
                            ]
                        }
                    )
                ]
            ) 
        },
    )

    def put(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            data_serializer = CommentSerializer(data=request.data)
            if data_serializer.is_valid():
                comment.content = data_serializer.validated_data["content"]
                comment.save()
                response_serializer = CommentSerializerResponse(comment)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not the owner of this comment'}, status=status.HTTP_403_FORBIDDEN)
        
        
class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=["Blog"],
        summary="Delete a comment",
        responses={
            204: OpenApiResponse(
                description="Comment deleted successfully"
            ),
            403: OpenApiResponse(
                description="Forbidden",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "message": "You are not the owner of this comment"
                        }
                    )
                ]
            ) 
        },
    )

    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You are not the owner of this comment'}, status=status.HTTP_403_FORBIDDEN)



