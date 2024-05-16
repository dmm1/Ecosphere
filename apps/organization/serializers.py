from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Country, Group, Team, CountrySetting

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'countries', 'country']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'group', 'created_by']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'countryadmin']

class CountrySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountrySetting
        fields = ['country', 'currency', 'timezone', 'language']