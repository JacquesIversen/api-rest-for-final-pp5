from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Issue, Comment, Like, DisLike
from .serializers import IssueSerializer, CommentSerializer, CommentDetailSerializer, DisLikeSerializer, LikeSerializer
from django.http import Http404
from rest_framework import status, permissions, generics
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



""" Views for Comments  """
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()


""" views for Likes & Dislikes: """
class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DisLikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = DisLikeSerializer
    queryset = DisLike.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

class DisLikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = DisLikeSerializer
    queryset = DisLike.objects.all()