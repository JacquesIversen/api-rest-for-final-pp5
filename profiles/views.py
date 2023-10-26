from rest_framework import generics
from pp5_api.permissions import IsOwnerOrReadOnly
from core.models import Profile
from .serializers import ProfileSerializer


""" Serializer for det user Profile """
class ProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer