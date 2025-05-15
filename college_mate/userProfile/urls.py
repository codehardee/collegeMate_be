from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileSetUpViewSet, get_my_profile

router = DefaultRouter()
router.register(r'profiles', StudentProfileSetUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', get_my_profile, name='get-my-profile'),
]