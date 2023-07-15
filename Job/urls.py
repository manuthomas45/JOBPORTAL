from django.urls import path
from Job import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("home/",views.CandidateIndexView.as_view(),name="home"),
    path("logout/",views.SignOutView,name="signout"),
    path('home/employer/',views.EmployerIndexView.as_view(),name='employer-home'),
    path('company/profile/create/',views.CompanyProfileCreateView.as_view(),name='companyprofile-create'),
    path('company/profile/<int:pk>/edit/',views.CompanyProfileEditView.as_view(),name='companyprofile-edit'),
    path('company/profile/details/',views.CompanyProfileView.as_view(),name='company-profile'),
    path('job/add/',views.JobAddView.as_view(),name='job-add'),
    path('job/<int:pk>/edit',views.JobEditView.as_view(),name='job-edit'),
    path('job/list/',views.MyJobListView.as_view(),name='myjob-list'),
    path('job/<int:id>/delete/',views.JobDeleteView.as_view(),name='job-delete'),
    path('job/<int:id>/details/',views.JobDetailView.as_view(),name='job-details'),
    path('job/<int:id>/application/add/',views.CandidateApplicationView.as_view(),name='application-add'),
    path('job/<int:id>/application/cancel',views.ApplicationCancelView.as_view(),name='application-cancel'),
    path('job/<int:id>/application/list/',views.ApplicationListView.as_view(),name='application-list'),
    path('job/<int:id>/application/accepted/list/',views.AcceptedApplicationsListView.as_view(),name='acceptedapplication-list'),
    path('applied-job/list',views.AppliedJobListView.as_view(),name='appliedjob-list'),
    path('applied-job/list',views.PendingJobListView.as_view(),name='appliedjob-list'),
    path('applied-job/list',views.AcceptedJobListView.as_view(),name='appliedjob-list'),
    path('candidate/profile/create/',views.CandidateProfileCreateView.as_view(),name='candidateprofile-create'),
    path('candidate/profile/<int:pk>/edit',views.CandidateProfileUpdateView.as_view(),name='candidateprofile-edit'),
    path('candidate/profile/details/',views.CandidateProfileDetailsView.as_view(),name='candidateprofile-details'),
    path('application/<int:id>candidate/details/',views.CandidateDetailsView.as_view(),name='candidate-details'),
    path('job/all/list/',views.JobListView.as_view(),name='job-list'),
    path('application/<int:id>/accept/',views.ApplicationAcceptView.as_view(),name='application-accept'),
    path('application/<int:id>/reject/',views.ApplicationRejectView.as_view(),name='application-reject'),
    path('error/',views.ErrorPageView.as_view(),name='error'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)