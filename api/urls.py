from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
router=DefaultRouter()
router.register("accounts/users",views.UsersView,basename="users")
router.register("users/cantidateprofile",views.CandidateProfileView,basename="cantidateprofile")
router.register("users/companyprofile",views.CompanyProfileView,basename="companyprofile")
router.register("jobs",views.JobView,basename="jobs")
router.register("applications",views.ApplicationView,basename="applications")

urlpatterns=[
    path("token/",ObtainAuthToken.as_view()),
    # path("token/",TokenObtainPairView.as_view()),
    # path("token/refresh/",TokenRefreshView.as_view())
]+router.urls