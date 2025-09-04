from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
urlpatterns = [
    path('', include(router.urls)),
]

# Available routes:
# GET /profiles/ - List all profiles (authenticated users only)
# GET /profiles/{username}/ - Retrieve a specific profile (authenticated users only)
# PUT /profiles/{username}/ - Update/Partially update a specific profile (authenticated users only, owner only)
