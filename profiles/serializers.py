from rest_framework import serializers, generics
from core.models import Profile, Issue, Comment
from core.serializers import IssueSerializer, CommentSerializer


class ProfileSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'age', 'name', 'biography',
            'issues', 'image', 'comments'
        ]
#'issues_posted', 'issues_solved', 'issues_listed'

    def get_issues(self, obj):

        issues = Issue.objects.filter(
            owner=obj.owner
        )
        return IssueSerializer(issues, many=True).data

    def get_comments(self, obj):

        comments = Comment.objects.filter(
            owner=obj.owner
        )
        return CommentSerializer(comments, many=True).data
