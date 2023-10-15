from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Issue
from .serializers import IssueSerializer
from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class IssueView(APIView):
    serializer_class = IssueSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    
    def get(self, request):
        issues = Issue.objects.all()
        serializer = IssueSerializer(
            issues, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = IssueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class IssueDetail(APIView):
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            issue = Issue.objects.get(pk=pk)
            self.check_object_permissions(self.request, issue)
            return issue
        except Issue.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        issue = self.get_object(pk)
        serializer = IssueSerializer(
            issue, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        issue = self.get_object(pk)
        serializer = IssueSerializer(
            issue, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)