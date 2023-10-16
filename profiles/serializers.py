from rest_framework import serializers, generics
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owned_cars = serializers.ReadOnlyField()
    issues_posted = serializers.ReadOnlyField()
    issues_solved = serializers.ReadOnlyField()
    is_owner = serializers.SerializerMethodField()
    issues_listed = serializers.ReadOnlyField()


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'age', 'name', 'biography', 'owned_cars', 'issues_posted', 'issues_solved', 'image', 'is_owner', 'issues_listed'
        ]