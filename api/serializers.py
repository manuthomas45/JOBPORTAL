from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from api.models import User,CandidateProfile,Job,CompanyProfile,Application

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password","role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CandidateProfileSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=UserSerializer(read_only=True)
    class Meta:
        model=CandidateProfile
        fields='__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=CompanyProfile
        fields='__all__'

class JobSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    company=CompanyProfileSerializer(read_only=True)
    start_date=serializers.CharField(read_only=True)
    class Meta:
        model=Job
        fields='__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    company=CompanyProfileSerializer(read_only=True)
    job=JobSerializer(read_only=True)
    # candidate=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    apply_date=serializers.CharField(read_only=True)
    is_active=serializers.CharField(read_only=True)
    class Meta:
        model=Application
        fields=["id","company","job","status","apply_date",'is_active']