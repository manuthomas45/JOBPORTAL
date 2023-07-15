from django import forms
from django.contrib.auth.models import AbstractUser
from api.models import CandidateProfile,CompanyProfile,User,Job
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2","role"]
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'Enter your firstname','class':'form-control'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Enter your lastname','class':'form-control'}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter your email','class':'form-control'}),
            'username':forms.TextInput(attrs={'placeholder':'Enter your firstname','class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'placeholder':'Enter your firstname','class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'placeholder':'Enter your firstname','class':'form-control'}),
            'role':forms.RadioSelect(attrs={'placeholder':'Enter your firstname','class':'form-control'}),


        }


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class CandidateProfileForm(forms.ModelForm):

    class Meta:
        model=CandidateProfile
        fields=["image","gender","phone","location","ready_to_relocate","qualification","skills","experience","resume",'description']
        widgets={
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.RadioSelect(),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'ready_to_relocate':forms.CheckboxInput(attrs={'value':'true'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'skills':forms.TextInput(attrs={'class':'form-control'}),
            'experience':forms.TextInput(attrs={'class':'form-control'}),
            'resume':forms.FileInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'})
        }
class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model=CompanyProfile
        fields=["company_name","logo","phone","location","adress","description"]
        widgets={
            'logo':forms.FileInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'company_name':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'adress':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),

        }
class JobForm(forms.ModelForm):

    class Meta:
        model=Job
        fields=["end_date","title","salary","description","qualification","experience","location","skills","job_type","vacancies"]
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'skills':forms.TextInput(attrs={'class':'form-control'}),
            'experience':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'job_type':forms.TextInput(attrs={'class':'form-control'}),
            'vacancies':forms.TextInput(attrs={'class':'form-control'}),
            'salary':forms.TextInput(attrs={'class':'form-control'}),
            'end_date':forms.TextInput(attrs={'class':'form-control'})
        }



# class ApplicationForm(forms.ModelForm):
    
#     class Meta:
#         model=Application
#         fields=["options"]