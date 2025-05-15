from rest_framework import viewsets, status
from .serializers import StudentProfileSetUpSerializer
from .models import StudentProfileSetUp
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    try:
        profile = StudentProfileSetUp.objects.get(student=request.user)
        serializer = StudentProfileSetUpSerializer(profile)
        return Response(serializer.data)
    except StudentProfileSetUp.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=404)


class StudentProfileSetUpViewSet(viewsets.ModelViewSet):
    queryset = StudentProfileSetUp.objects.all()
    serializer_class = StudentProfileSetUpSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the authenticated user to the student profile
        student = self.request.user

        # Ensure the user is associated with a valid student_id
        if not hasattr(student, 'student_id'):
            raise ValueError("Authenticated user does not have a valid student_id.")

        # Save the profile with the authenticated student
        serializer.save(student=student)

#
# from rest_framework import viewsets, status
# from .serializers import StudentProfileSetUpSerializer
# from .models import StudentProfileSetUp
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
#
# class StudentProfileSetUpViewSet(viewsets.ModelViewSet):
#     queryset = StudentProfileSetUp.objects.all()
#     serializer_class = StudentProfileSetUpSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         # Using the serializer with the context of the authenticated user
#         serializer = StudentProfileSetUpSerializer(data=request.data, context={'request': request})
#
#         if serializer.is_valid():
#             serializer.save()  # This will automatically assign the student
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
