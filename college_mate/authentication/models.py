from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class StudentAccountManager(BaseUserManager):
    def create_user(self, student_id, password=None, **extra_fields):
        if not student_id:
            raise ValueError('The Student ID field must be set')
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, **extra_fields):
        # extra_fields.setdefault('is_default', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(student_id, password, **extra_fields)

class StudentAccountCreation(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    student_id = models.CharField(max_length=8, unique=True, primary_key=True)  # primary key
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = StudentAccountManager()

    USERNAME_FIELD = 'student_id'  # This should be a string
    REQUIRED_FIELDS = ['first_name', 'password', 'email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.student_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student_id




# Create your models here.
