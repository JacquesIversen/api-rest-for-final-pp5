from django.db.models import Count
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Issue, Comment, Like, DisLike
from .serializers import IssueSerializer, CommentSerializer, CommentDetailSerializer, DisLikeSerializer, LikeSerializer
from rest_framework import permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend



""" Views for IssueList/View  """
class IssueView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Issue.objects.annotate(
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
        'car',
        'model',
        'year',
        'engine_size',
        'description',
    ]
    ordering_fields = ['car',
        'model',
        'year',
        'engine_size',
        'comments',]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Issue.objects.annotate(
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')




""" Views for Comments  """
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.annotate(
        likes_count=Count('likes', distinct=True),
        dislikes_count=Count('dislikes', distinct=True),
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.annotate(
        likes_count=Count('likes', distinct=True),
        dislikes_count=Count('dislikes', distinct=True),
    )


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