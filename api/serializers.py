from rest_framework import serializers
from authenticate.models import *
from homedash.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
