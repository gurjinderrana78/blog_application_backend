from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class Posts(APIView):
    http_method_names = ['get', 'post']
    pagination_class = Paginator  # Set default pagination class

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        # Retrieve all posts or filter based on query parameters
        posts = Post.objects.all()  # Adjust filtering logic as needed

        # Apply pagination using request parameters
        page_size = request.GET.get('page_size', 10)  # Default to 10 posts per page
        page_number = request.GET.get('page', 1)  # Default to page 1

        paginator = Paginator(posts, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = PostSerializer(page_obj, many=True)

        # Create a well-structured response dictionary with pagination data
        response_data = {
            'data': serializer.data,
            'pagination': {
                'total_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'has_prev': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }

        return Response(response_data)


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
        
    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            try:
                post = Post.objects.get(id=id)
            except Post.DoesNotExist:
                return Response({'error': 'Post Does not exist'}, status=status.HTTP_404_NOT_FOUND)
            try:
                all_comments = Comment.objects.filter(post_id=id)
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
    
    def delete(self, request, id=None, *args, **kwargs):
        if id is not None:
            try:
                comment = Comment.objects.get(id= id)
                deleted = comment.delete()
                if deleted:
                   return Response({'message': 'Comment successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
                else:
                   return Response({'error': 'Failed to delete comment'}, status=status.HTTP_400_BAD_REQUEST)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Comment Not found'}, status=status.HTTP_404_NOT_FOUND)
        

    