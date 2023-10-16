from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Issue, Comment, Like, DisLike
from .serializers import IssueSerializer, CommentSerializer, CommentDetailSerializer, DisLikeSerializer, LikeSerializer
from rest_framework import status, permissions, generics



""" Views for IssueList/View  """
class IssueView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Issue.objects.all()




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