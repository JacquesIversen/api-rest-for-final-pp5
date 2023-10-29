from rest_framework import serializers
from core.models import Profile, Issue, Comment
from core.serializers import IssueSerializer, CommentSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for the Profile model."""
    issues = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'age', 'name', 'biography',
            'issues', 'image', 'comments',
            'email', 'date_joined',
        ]

    def get_date_joined(self, obj):
        """ Get the date joined of the current profile."""
        return naturaltime(obj.owner.date_joined)

    def get_email(self, obj):
        """ Get the email of the current profile."""
        return obj.owner.email

    def get_issues(self, obj):
        """ Get the issues of the current profile."""
        issues = Issue.objects.filter(
            owner=obj.owner
        )
        return IssueSerializer(issues, many=True).data

    def get_comments(self, obj):
        """ Get the comments of the current profile."""
        comments = Comment.objects.filter(
            owner=obj.owner
        )
        return CommentSerializer(comments, many=True).data
