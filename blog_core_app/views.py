from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class Posts(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            try:
                individual_post = Post.objects.get(id=id)
                serializer = PostSerializer(individual_post)
                return Response(serializer.data)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            all_posts = Post.objects.all()
            serializer = PostSerializer(all_posts, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id=None, *args, **kwargs):
        try:
            individual_post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
           
        serializer = PostSerializer(instance=individual_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None, *args, **kwargs):
        try:
            individual_post = Post.objects.get(id=id)
        except Post.DoesNotExist:
           return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        deleted = individual_post.delete()
        if deleted:
           return Response({'message': 'Post successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error': 'Failed to delete post'}, status=status.HTTP_400_BAD_REQUEST)


class Comments(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
        
    def get(self, request, post_id=None, *args, **kwargs):
        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({'error': 'Post Does not exist'}, status=status.HTTP_404_NOT_FOUND)
            try:
                all_comments = Comment.objects.filter(post_id=post_id)
                serializer = CommentSerializer(all_comments, many = True)
                return Response(serializer.data)
            except Comment.DoesNotExist:
                return Response({'error': 'No comments for this post'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Post not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id = None, *args, **kwargs):
        if comment_id is not None:
            try:
                comment = Comment.objects.get(id= comment_id)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment Not found'}, status=status.HTTP_404_NOT_FOUND)
        deleted = comment.delete()
        if deleted:
           return Response({'message': 'Comment successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
           return Response({'error': 'Failed to delete comment'}, status=status.HTTP_400_BAD_REQUEST)
        

    