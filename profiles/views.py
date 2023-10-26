from rest_framework import generics, views
from pp5_api.permissions import IsOwnerOrReadOnly
from core.models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response


""" Serializer for det user Profile """
class ProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class MyProfile(views.APIView):
    """View that givies user based on access token"""
    serializer_class = ProfileSerializer

    def get(self, request):

        profile = Profile.objects.filter(
            owner=request.user
        ).first()

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=200)