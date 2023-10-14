from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owned_cars = serializers.ReadOnlyField()
    issues_posted = serializers.ReadOnlyField()
    issues_solved = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'name', 'age', 'biography', 'owned_cars', 'issues_posted', 'issues_solved', 'image',
        ]