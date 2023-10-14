from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

""" Serializer for det user Profile """
class ProfileView(APIView):
    
    def get(self, request):
        profileObjects = Profile.objects.all()
        serializer = ProfileSerializer(profileObjects, many=True)
        return Response(serializer.data)