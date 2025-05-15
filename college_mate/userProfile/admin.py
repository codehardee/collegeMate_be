from django.contrib import admin
from .models import StudentProfileSetUp

@admin.register(StudentProfileSetUp)
class StudentProfileSetUpAdmin(admin.ModelAdmin):
    pass

# Register your models here.
