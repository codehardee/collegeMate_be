from django.db import models

from authentication.models import StudentAccountCreation


class StudentProfileSetUp(models.Model):
    unique_student_id = models.CharField(max_length=8, unique=True)  # Optional, to store student_id separately
    student = models.ForeignKey(StudentAccountCreation, to_field='student_id', on_delete=models.CASCADE,
                                related_name='profiles')
    about = models.TextField(max_length=500, blank=True, null=True)
    interests = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    portfolio = models.FileField(upload_to='portfolio/', blank=True, null=True)
    social_media = models.URLField(blank=True, null=True)
    skills = models.CharField(max_length=150, blank=True, null=True)
    certificate = models.FileField(upload_to='certificate/', blank=True, null=True)
    education = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.student_id}"
