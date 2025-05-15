from django.contrib import admin
from .models import uploadProject

@admin.register(uploadProject)
class uploadProjectAdmin(admin.ModelAdmin):
    pass

# Register your models here.
