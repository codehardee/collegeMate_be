# your_app/authentication_backends.py

from django.contrib.auth.backends import ModelBackend
from .models import StudentAccountCreation


class StudentAccountBackend(ModelBackend):
    def authenticate(self, request, student_id=None, username=None, password=None, **kwargs):
        if student_id:
            try:
                user = StudentAccountCreation.objects.get(student_id=student_id)
            except StudentAccountCreation.DoesNotExist:
                return None
        elif username:
            try:
                user = StudentAccountCreation.objects.get(username=username)
            except StudentAccountCreation.DoesNotExist:
                return None
        else:
            return None

        if user.check_password(password):
            return user
        return None
