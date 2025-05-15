from django.contrib import admin
from .models import StudentAccountCreation

@admin.register(StudentAccountCreation)
class StudentAccountCreationAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'is_active', 'is_staff')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('student_id',)
    fieldsets = (
        (None, {
            'fields': ('student_id', 'password', 'first_name', 'last_name', 'email', 'phone', 'username')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )