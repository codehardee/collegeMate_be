from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import permissions
from .models import uploadProject, Bid
from .serializers import uploadProjectSerializer, BidSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # queryset = uploadProject.objects.filter(deleted=False)
    serializer_class = uploadProjectSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # if self.request.method in ['GET']:
        #     return [AllowAny()]  # ✅ should be a class instance, this is actually fine, but not the issue

        # But this might fail due to side-effects. So instead use the preferred style:
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return uploadProject.objects.filter(deleted=False)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        return Response({
            "status":"You have successfully listed the project."
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        return Response({
            "status": "Project updated successfully.",
            "project": uploadProjectSerializer(instance).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def delete(self, request, pk=None):
        project = self.get_object()
        if project.student != request.user:
            return Response({"error": "You do not have permission to delete this project."},
                            status=status.HTTP_403_FORBIDDEN)
        project.deleted = True
        project.save()
        return Response({"status": "Project soft deleted."}, status=status.HTTP_204_NO_CONTENT)

# to bid the project
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
#
# from . import permissions
# from .models import uploadProject, Bid
# from .serializers import uploadProjectSerializer, BidSerializer
# from .permissions import IsOwnerOrReadOnly
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# class ProjectViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     queryset = uploadProject.objects.filter(deleted=False)
#     serializer_class = uploadProjectSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return uploadProject.objects.filter(deleted=False)
#
#     def perform_create(self, serializer):
#         serializer.save(student=self.request.user)
#         return Response({
#             "status":"You have successfully listed the project."
#         }, status=status.HTTP_200_OK)
#
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         return Response({
#             "status": "Project updated successfully.",
#             "project": uploadProjectSerializer(instance).data
#         }, status=status.HTTP_200_OK)
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def delete(self, request, pk=None):
#         project = self.get_object()
#         if project.student != request.user:
#             return Response({"error": "You do not have permission to delete this project."},
#                             status=status.HTTP_403_FORBIDDEN)
#         project.deleted = True
#         project.save()
#         return Response({"status": "Project soft deleted."}, status=status.HTTP_204_NO_CONTENT)
#
# # to bid the project
# class BidViewSet(viewsets.ModelViewSet):
#     queryset = Bid.objects.all()
#     serializer_class = BidSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(student=self.request.user)
