from django.db import models
from authentication.models import StudentAccountCreation


class uploadProject(models.Model):
    LARGE = 'large'
    MEDIUM = 'medium'
    SMALL = 'small'
    SCOPE_CHOICES = [
        (LARGE, 'Large'),
        (MEDIUM, 'Medium'),
        (SMALL, 'Small'),
    ]
    HOURLY = 'hourly'
    FIXED = 'fixed'
    PRICE_CHOICES = [
        (HOURLY, 'Hourly'),
        (FIXED, 'Fixed'),
    ]

    title = models.CharField(max_length=200)
    skills = models.CharField(max_length=200)
    scope = models.CharField(max_length=30, choices=SCOPE_CHOICES)
    price = models.CharField(max_length=20, choices=PRICE_CHOICES)
    description = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Bid(models.Model):
    project = models.ForeignKey(uploadProject, on_delete=models.CASCADE, related_name='bids')
    student = models.ForeignKey(StudentAccountCreation, on_delete=models.CASCADE)  # Reference to your custom user model
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid by {self.student.student_id} on {self.project.title}'


