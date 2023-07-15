from django.shortcuts import render,redirect
from api.models import User,CandidateProfile,CompanyProfile,Job,Application
from Job.forms import RegistrationForm,LoginForm,CompanyProfileForm,JobForm,CandidateProfileForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


def employersignin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.role=='employer':
            return fn(request,*args,**kwargs)
        else:
            return redirect('error')
    return wrapper

employerdecs=[employersignin_required,never_cache]

def candidatesignin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.role=='candidate':
            
            return fn(request,*args,**kwargs)
        else:
            return redirect('error')       
    return wrapper

candidatedecs=[candidatesignin_required,never_cache]



class SignUpView(CreateView):

    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")



class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            usrn=form.cleaned_data.get("username")
            passw=form.cleaned_data.get("password")
            usr=authenticate(request,username=usrn,password=passw)
            if usr:
                
                login(request,usr)
                if request.user.role == 'employer':
                    if CompanyProfile.objects.filter(user_id=request.user.id):
                        return redirect('employer-home')
                    else:
                        return redirect("companyprofile-create")
                elif request.user.role == 'candidate':
                    if CandidateProfile.objects.filter(user_id=request.user.id):
                        return redirect('home')
                    else:
                        return redirect("candidateprofile-create")
            else:
                messages.error(request, 'Invalid username and passwod, Please try again.')
                return render(request,"login.html",{"form":form})
       

def SignOutView(request,*args,**kwargs):
    logout(request)
    return redirect('signin')
    
class ErrorPageView(TemplateView):
    template_name='errorpage.html'


#COMPANY

@method_decorator(employerdecs,name='dispatch')
class EmployerIndexView(TemplateView):
    template_name="employer-index.html"

@method_decorator(employerdecs,name='dispatch')
class CompanyProfileCreateView(CreateView):
    form_class=CompanyProfileForm
    template_name='company-profilecreate.html'
    model=CompanyProfile
    success_url=reverse_lazy('employer-home')


    def form_valid(self, form):
       
        form.instance.user=self.request.user
        messages.success(self.request,'company profile is created')
        return super().form_valid(form)

@method_decorator(employerdecs,name='dispatch')
class CompanyProfileEditView(UpdateView):
    form_class=CompanyProfileForm
    template_name='companyprofile-update.html'
    model=CompanyProfile
    success_url=reverse_lazy('company-profile')

@method_decorator(employerdecs,name='dispatch')
class CompanyProfileView(TemplateView):
    template_name='company-profiledetails.html'

@method_decorator(employerdecs,name='dispatch')
class JobAddView(CreateView):
    model=Job
    form_class=JobForm
    template_name='job-add.html'
    success_url=reverse_lazy('myjob-list')

    def form_valid(self, form):
        company=CompanyProfile.objects.get(user=self.request.user)
        form.instance.company=company
        return super().form_valid(form)
    
@method_decorator(employerdecs,name='dispatch')
class JobEditView(UpdateView):
    model=Job
    form_class=JobForm
    template_name='job-update.html'
    success_url=reverse_lazy('myjob-list')

@method_decorator(employerdecs,name='dispatch')
class MyJobListView(ListView):
    model=Job
    template_name='addedjob-list.html'
    context_object_name='jobs'

    def get_queryset(self):
        company=CompanyProfile.objects.get(user=self.request.user)
        return Job.objects.filter(company=company,is_active=True)

@method_decorator(employerdecs,name='dispatch')
class JobDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        job=Job.objects.filter(id=id)
        Job.objects.filter(id=id).update(is_active=False)
        return redirect('myjob-list')

@method_decorator(employerdecs,name='dispatch')
class ApplicationListView(ListView):
    model=Application
    template_name='application-list.html'
    context_object_name='apps'

    def get_queryset(self):
        id=self.kwargs.get('id')
        job=Job.objects.get(id=id)
        return Application.objects.filter(job=job,status='pending')
    

@method_decorator(employerdecs,name='dispatch')
class AcceptedApplicationsListView(ListView):
    model=Application
    template_name='acceptedapplications-list.html'
    context_object_name='apps'
    
    def get_queryset(self):
        id=self.kwargs.get('id')
        job=Job.objects.get(id=id)
        return Application.objects.filter(job=job,status='accept')


@method_decorator(employerdecs,name='dispatch') 
class CandidateDetailsView(ListView):
    model=Application
    template_name='candidatedetails.html'
    context_object_name='apps'

    def get_queryset(self):
        id=self.kwargs.get('id')
        return Application.objects.filter(id=id)
    
@method_decorator(employerdecs,name='dispatch') 
class ApplicationAcceptView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        app=Application.objects.get(id=id)
        email=app.candidate.user.email
        Application.objects.filter(id=id).update(status='accept')
        subject='reply for your jobapplication'
        message='Hi,your job application was accepted'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message,email_from,recipient_list)
        return redirect('myjob-list')
    
@method_decorator(employerdecs,name='dispatch')       
class ApplicationRejectView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        app=Application.objects.get(id=id)
        email=app.candidate.user.email
        Application.objects.filter(id=id).update(is_active=False,status='reject')
        subject='reply for your jobapplication'
        message='Hi,your job application was rejected'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message,email_from,recipient_list)
        return redirect('myjob-list')

# CANDIDATE

@method_decorator(candidatedecs,name='dispatch')
class CandidateIndexView(TemplateView):
    template_name="candidate-index.html"

@method_decorator(candidatedecs,name='dispatch')
class CandidateProfileCreateView(CreateView):
    form_class=CandidateProfileForm
    template_name='candidate-profilecreate.html'
    model=CandidateProfile
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        print(self.request.FILES)
        form.instance.user=self.request.user
        messages.success(self.request,'candidate profile is created')
        return super().form_valid(form)

@method_decorator(candidatedecs,name='dispatch')    
class CandidateProfileUpdateView(UpdateView):
    form_class=CandidateProfileForm
    template_name='candidateprofile-update.html'
    model=CandidateProfile
    success_url=reverse_lazy('candidateprofile-details')

@method_decorator(candidatedecs,name='dispatch')
class CandidateProfileDetailsView(TemplateView):
    template_name='candidateprofile-details.html'

class JobListView(ListView):
    model=Job
    template_name='alljob-list.html'
    context_object_name='jobs'

    def get_queryset(self):
        return Job.objects.filter(is_active=True)
    
class JobDetailView(ListView):
    model=Job
    template_name='job-details.html'
    context_object_name='job'

    def get_queryset(self):
        id=self.kwargs.get('id')
        return Job.objects.filter(id=id)

@method_decorator(candidatedecs,name='dispatch')
class CandidateApplicationView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        candidate=CandidateProfile.objects.get(user_id=request.user.id)
        job=Job.objects.get(id=id)
        Application.objects.create(job=job,candidate=candidate)
        return redirect("appliedjob-list")

@method_decorator(candidatedecs,name='dispatch')       
class ApplicationCancelView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        Application.objects.filter(id=id).update(is_active=False,status='cancelled')
        return redirect('appliedjob-list')

@method_decorator(candidatedecs,name='dispatch')
class AppliedJobListView(ListView):
    model=Application
    template_name='appliedjob-list.html'
    context_object_name='apps'
    
    def get_queryset(self):
        candidate=CandidateProfile.objects.get(user_id=self.request.user.id)
        return Application.objects.filter(candidate=candidate).exclude(status='cancelled')
    
@method_decorator(candidatedecs,name='dispatch')
class PendingJobListView(ListView):
    model=Application
    template_name='appliedjob-list.html'
    context_object_name='apps'
    
    def get_queryset(self):
        candidate=CandidateProfile.objects.get(user_id=self.request.user.id)
        return Application.objects.filter(candidate=candidate,status='pending')
 
@method_decorator(candidatedecs,name='dispatch')   
class RejectedJobListView(ListView):
    model=Application
    template_name='appliedjob-list.html'
    context_object_name='apps'
    
    def get_queryset(self):
        candidate=CandidateProfile.objects.get(user_id=self.request.user.id)
        return Application.objects.filter(candidate=candidate,status='reject')


@method_decorator(candidatedecs,name='dispatch')   
class AcceptedJobListView(ListView):
    model=Application
    template_name='appliedjob-list.html'
    context_object_name='apps'
    
    def get_queryset(self):
        candidate=CandidateProfile.objects.get(user_id=self.request.user.id)
        return Application.objects.filter(candidate=candidate,status='accept')
    
