from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
# class ProfileListView(generics.ListAPIView):
#     queryset = Profile.objects.select_related('user').all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ProfileDetailView(generics.RetrieveAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         username = self.kwargs.get('username')
#         user = get_object_or_404(User, username=username)
#         return get_object_or_404(Profile, user=user)

# class ProfileUpdateView(generics.UpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
#     def get_object(self):
#         username = self.kwargs.get('username')
#         user = get_object_or_404(User, username=username)
#         return get_object_or_404(Profile, user=user)

#! Using ViewSet for better organization
class ProfileViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, and updating user profiles.
    """
    lookup_field = 'username'
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        queryset = Profile.objects.select_related('user').all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, username=None):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def update(self, request, username=None):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)