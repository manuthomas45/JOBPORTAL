from django.shortcuts import render
from api.serializers import UserSerializer,CandidateProfileSerializer,CompanyProfileSerializer,JobSerializer,ApplicationSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,GenericViewSet,ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import authentication,permissions,serializers,views
from api.models import User,CandidateProfile,CompanyProfile,Job,Application
from rest_framework.decorators import action
from django.core.mail import send_mail


# from django.contrib.auth.models import AbstractUser,User
# Create your views here.

class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class CandidateProfileView(ModelViewSet):
    serializer_class=CandidateProfileSerializer
    queryset=CandidateProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CandidateProfile.objects.filter(user=self.request.user)
    
        

class CompanyProfileView(ModelViewSet):
    serializer_class=CompanyProfileSerializer
    queryset=CompanyProfile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)
        
class JobView(ModelViewSet):
    serializer_class=JobSerializer
    queryset=Job.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=self.request.user)
            serializer.save(company=company)
        else:
            raise serializers.ValidationError("not allowed to perform")
        
    def update(self, request, *args, **kwargs):
        job=self.get_object()
        if self.request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=request.user)
            if job.company == company:
                return super().update(request, *args, **kwargs)
            else:
                raise serializers.ValidationError('not allowed to perform')
        else:
            raise serializers.ValidationError('not allowed to perform')

    def get_queryset(self):
        if self.request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=self.request.user)
            return Job.objects.filter(company=company,is_active=True)
        else:
            return Job.objects.filter(is_active=True)
        
    def destroy(self, request, *args, **kwargs):
        job=self.get_object()
        if request.user.role == 'employer':
            company=CompanyProfile.objects.get(user=request.user)
            if job.company == company:
                job.is_active=False
                return Response('job deleted')
            else:
                raise serializers.ValidationError('not allowed to perform')
        else:
            raise serializers.ValidationError('not allowed to perform')

    @action(methods=['get'],detail=True)
    def apply(self,request,*args,**kwargs):
        job=self.get_object()
        if request.user.role == 'candidate' and job.is_active==True:
            candidate=CandidateProfile.objects.get(user=request.user)
            Application.objects.create(job=job,candidate=candidate)
            return Response('applied')
        else:
            raise serializers.ValidationError('not allowed to perform')
        

    @action(methods=['get'],detail=True)
    def application_list(self,request,*args,**kwargs):
        job=self.get_object()
        if request.user.role == 'employer':
            qs=Application.objects.filter(job=job)
            serializer=ApplicationSerializer(qs,many=True)
            return Response(data=serializer.data)
        else:
            raise serializers.ValidationError('not allowed to perform')



class ApplicationView(ModelViewSet):
    serializer_class=ApplicationSerializer
    queryset=Application.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError('not allowed to perform')
    
    def update(self, request, *args, **kwargs):
        return serializers.ValidationError('not allowed to perform')
    
    def list(self, request, *args, **kwargs):
        if self.request.user.role == 'candidate':
            cand=CandidateProfile.objects.get(user=self.request.user)
            qs=Application.objects.filter(candidate=cand,is_active=True)
            serializer=ApplicationSerializer(qs,many=True)
            return Response(data=serializer.data)
        else:
            raise serializers.ValidationError('not allowed to perform')


    def retrieve(self, request, *args, **kwargs):
        app=self.get_object()
        if request.user.role == 'candidate':
            cand=CandidateProfile.objects.get(user=request.user)
            if app.candidate == cand and app.is_active == True:
                serializer=ApplicationSerializer(app,many=False)
                return Response(data=serializer.data)
            else:
                raise serializers.ValidationError('not allowed to perform')
        else:
            comp=CompanyProfile.objects.get(user=request.user)
            if app.job.company == comp and app.is_active == True:
                serializer=ApplicationSerializer(app,many=False)
                return Response(data=serializer.data)
            else:
                raise serializers.ValidationError('not allowed to perform')
            
    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'candidate':
            app=self.get_object()
            app.status='cancelled'
            app.is_active=False
            return Response('application cancelled')
        else:
            raise serializers.ValidationError('not allowed to perform')

    @action(methods=['get'],detail=True)
    def accept(self,request,*args,**kwargs):
        app=self.get_object()
        app.status='accept'
        app.save()
        return Response('accepted')
    
    @action(methods=['get'],detail=True)
    def reject(self,request,*args,**kwargs):
        app=self.get_object()
        app.status='reject'
        app.is_active=False
        app.save()
        return Response('rejected')


