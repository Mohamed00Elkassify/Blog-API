from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
	path('', include(router.urls)),
]

# Available routes:
# Categories (read-only)
#   GET /categories/ - List categories
#   GET /categories/{id}/ - Retrieve category
# Tags (read-only)
#   GET /tags/ - List tags
#   GET /tags/{id}/ - Retrieve tag
# Posts
#   GET /posts/ - List posts (supports filter, search, ordering)
#   POST /posts/ - Create post (auth)
#   GET /posts/{id}/ - Retrieve post
#   PUT /posts/{id}/ - Update post (author only)
#   PATCH /posts/{id}/ - Partial update post (author only)
#   DELETE /posts/{id}/ - Delete post (author only)
#   POST /posts/{id}/like/ - Toggle like on post
#   GET /posts/{id}/comments/ - List comments for post
#   POST /posts/{id}/comments/ - Add comment to post
# Comments
#   GET /comments/ - List comments
#   POST /comments/ - Create comment
#   GET /comments/{id}/ - Retrieve comment
#   PUT /comments/{id}/ - Update comment (author only)
#   PATCH /comments/{id}/ - Partial update comment (author only)
#   DELETE /comments/{id}/ - Delete comment (author only)
#   POST /comments/{id}/like/ - Toggle like on comment