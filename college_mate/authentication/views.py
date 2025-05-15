from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentAccountCreation
from .serializers import StudentAccountSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# from userProfile.models import StudentProfileSetUp

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from userProfile.models import StudentProfileSetUp


class CustomTokenObtainPairView(TokenObtainPairView):
    """
       Obtain JWT token pairs (access & refresh).
    """
    serializer_class = CustomTokenObtainPairSerializer


class StudentAccountCreateView(generics.CreateAPIView):
    """
    Create a new student account.
    """
    queryset = StudentAccountCreation.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [AllowAny]


    def perform_create(self, serializer):
        student = serializer.save()
        StudentProfileSetUp.objects.create(
            student=student,
            unique_student_id=student.student_id
        )

    # No need to redefine the 'post' method; the parent class already provides it.



class StudentAccountListView(generics.ListAPIView):
    """
       List all student accounts (Requires authentication).
    """
    queryset = StudentAccountCreation.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [IsAuthenticated]

class StudentAccountDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific student account.
    """
    queryset = StudentAccountCreation.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [IsAuthenticated]



class StudentAccountUpdateView(generics.UpdateAPIView):
    queryset = StudentAccountCreation.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [IsAuthenticated]

# delete from administration
class StudentAccountDeleteView(generics.DestroyAPIView):
    """
    Update a student account.
    """
    queryset = StudentAccountCreation.objects.all()
    serializer_class = StudentAccountSerializer
    permission_classes = [IsAdminUser]




# soft delete at user side
class DeleteStudentAccount(APIView):
    """
    Permanently delete a student account (Admin only).
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.is_deleted = True
        user.save()
        return Response({"result":"user deleted."})


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            student_id = serializer.validated_data.get('student_id')
            password = serializer.validated_data['password']

            if username:
                user = authenticate(username=username, password=password)
            elif student_id:
                user = authenticate(student_id=student_id, password=password)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if user is not None:
                login(request, user)
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
