from django.urls import path
from .views import (StudentAccountCreateView, StudentAccountListView,
    StudentAccountDetailView,
    StudentAccountUpdateView,
    StudentAccountDeleteView,
    DeleteStudentAccount,
    LoginView,
    CustomTokenObtainPairView
    )

urlpatterns = [
    path('signup/', StudentAccountCreateView.as_view(), name='student-signup'),
    path('students/', StudentAccountListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentAccountDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', StudentAccountUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', StudentAccountDeleteView.as_view(), name='student-delete'),
    path('delete-account/', DeleteStudentAccount.as_view(), name='delete-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
