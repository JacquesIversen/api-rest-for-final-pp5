from rest_framework import serializers
from django.db import IntegrityError
from .models import Issue, Comment, Like, DisLike
from django.contrib.humanize.templatetags.humanize import naturaltime


class IssueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        # request = self.context['request']
        return None

    class Meta:
        model = Issue
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at',
            'title', 'car', 'model', 'year', 'engine_size',
            'description', 'is_solved', 'image', 'comments_count',
        ]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    dislike_id = serializers.SerializerMethodField()
    dislikes_count = serializers.ReadOnlyField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return None

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_like_id(self, obj):
        return 1

    def get_dislike_id(self, obj):
        return 1

    # get the user's profiles who liked the comment
    def get_likes(self, obj):
        likes = obj.likes.all()
        return LikeSerializer(likes, many=True).data

    def get_dislikes(self, obj):
        dislikes = obj.dislikes.all()
        return DisLikeSerializer(dislikes, many=True).data

    class Meta:
        model = Comment
        fields = [
            'issue', 'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'comment_area', 'created_at', 'like_id', "likes_count", 'dislikes',
            'dislikes_count', 'likes', 'dislike_id',
        ]


class CommentDetailSerializer(CommentSerializer):
    issue = serializers.ReadOnlyField(source='issue.id')


""" Here follows Like & Dislike Serializers: """


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'comment']

    def create(self, validated_data):
        try:
            like = Like.objects.get(
                owner=validated_data['owner'],
                comment=validated_data['comment']
            )
            like.delete()
            return Like(id=None)

        except Like.DoesNotExist:
            if validated_data['owner'] == validated_data['comment'].owner:
                raise serializers.ValidationError({
                    'detail': 'You cannot like your own comment.'
                })
            try:
                dislike = DisLike.objects.get(
                    owner=validated_data['owner'],
                    comment=validated_data['comment']
                )
                dislike.delete()
            except DisLike.DoesNotExist:
                pass

            return super().create(validated_data)


class DisLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DisLike
        fields = ['id', 'created_at', 'owner', 'comment']

    def create(self, validated_data):

        try:
            dislike = DisLike.objects.get(
                owner=validated_data['owner'],
                comment=validated_data['comment']
            )
            dislike.delete()

            return DisLike(id=None)
        except DisLike.DoesNotExist:

            if validated_data['owner'] == validated_data['comment'].owner:
                raise serializers.ValidationError({
                    'detail': 'You cannot dislike your own comment.'
                })

            try:
                like = Like.objects.get(
                    owner=validated_data['owner'],
                    comment=validated_data['comment']
                )
                like.delete()
            except Like.DoesNotExist:
                pass

            return super().create(validated_data)
