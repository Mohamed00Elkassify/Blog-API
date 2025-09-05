from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Category, Tag, Post, Comment, PostLike, CommentLike
from .serializers import CategorySerializer, TagSerializer, PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        tags=['Categories'],
        summary='List categories',
        description='Get all content categories available for posts. Authentication required.'
    ),
    retrieve=extend_schema(
        tags=['Categories'],
        summary='Get category details',
        description='Retrieve a single category by ID.'
    )
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing categories.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(
        tags=['Tags'],
        summary='List tags',
        description='Get all content tags available for posts. Authentication required.'
    ),
    retrieve=extend_schema(
        tags=['Tags'],
        summary='Get tag details',
        description='Retrieve a single tag by ID.'
    )
)
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing tags.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(
        tags=['Posts'],
        summary='List posts',
        description='Get posts with filtering, search, and ordering. Query params: ?category__slug=tech&tags__slug=django&search=term&ordering=-created_at'
    ),
    create=extend_schema(
        tags=['Posts'],
        summary='Create a post',
        description='Create a new blog post. Author is automatically set to the authenticated user.'
    ),
    retrieve=extend_schema(
        tags=['Posts'],
        summary='Get post details',
        description='Retrieve a single post with all details including tags, category, and like count.'
    ),
    update=extend_schema(
        tags=['Posts'],
        summary='Update post (PUT)',
        description='Full update of a post. Only the author can modify their posts.'
    ),
    partial_update=extend_schema(
        tags=['Posts'],
        summary='Update post (PATCH)',
        description='Partial update of a post. Only the author can modify their posts.'
    ),
    destroy=extend_schema(
        tags=['Posts'],
        summary='Delete post',
        description='Delete a post. Only the author can delete their posts.'
    ),
    like=extend_schema(
        tags=['Posts'],
        summary='Toggle like on post',
        description='Like a post if not already liked, unlike if already liked. Returns new like count.'
    ),
    comments=extend_schema(
        tags=['Posts'],
        summary='Post comments',
        description='GET: List comments for this post. POST: Add a new comment to this post.'
    )
)
class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on blog posts.
    """
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags').all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'author__username']
    search_fields = ['title', 'content', 'author__username', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        # If the like already exists, we can choose to unlike
        if not created:
            like.delete()
            return Response({'status': 'unliked', 'likes_count': post.likes_count})
        return Response({'status': 'liked', 'likes_count': post.likes_count}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.select_related('author').all().order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post) #* Associate comment with post and author
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema_view(
    list=extend_schema(
        tags=['Comments'],
        summary='List comments',
        description='Get all comments across all posts, ordered by newest first.'
    ),
    create=extend_schema(
        tags=['Comments'],
        summary='Create a comment',
        description='Create a new comment. Author is automatically set to the authenticated user. Must specify post ID.'
    ),
    retrieve=extend_schema(
        tags=['Comments'],
        summary='Get comment details',
        description='Retrieve a single comment with author info and like count.'
    ),
    update=extend_schema(
        tags=['Comments'],
        summary='Update comment (PUT)',
        description='Full update of a comment. Only the author can modify their comments.'
    ),
    partial_update=extend_schema(
        tags=['Comments'],
        summary='Update comment (PATCH)',
        description='Partial update of a comment. Only the author can modify their comments.'
    ),
    destroy=extend_schema(
        tags=['Comments'],
        summary='Delete comment',
        description='Delete a comment. Only the author can delete their comments.'
    ),
    like=extend_schema(
        tags=['Comments'],
        summary='Toggle like on comment',
        description='Like a comment if not already liked, unlike if already liked. Returns new like count.'
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on comments.
    """
    queryset = Comment.objects.select_related('author', 'post').prefetch_related('likes').all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            like.delete()
            return Response({'status': 'unliked', 'likes_count': comment.likes_count})
        return Response({'status': 'liked', 'likes_count': comment.likes_count})