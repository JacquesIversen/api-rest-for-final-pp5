from django.db.models import Count
from rest_framework import generics
from pp5_api.permissions import IsOwnerOrReadOnly
from core.models import Profile
from .serializers import ProfileSerializer



class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.annotate(
        issues_count=Count('owner__issue', distinct=True),).order_by('-created_at')
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        issues_count=Count('owner__issue', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer