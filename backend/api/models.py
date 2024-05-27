from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # Add custom fields here
    surname = models.TextField(max_length=500, blank=True)
    username = models.TextField(max_length=500, blank=True, unique=True)
    id_number = models.TextField(max_length=13, blank=True, unique=True)
    nationality = models.TextField(max_length=500, null=True)
    email = models.TextField(max_length=500, blank=True, unique=True)
    bank = models.TextField(max_length=500, blank=True)
    acc = models.TextField(max_length=500, blank=True)
    phoneNumber = models.TextField(max_length=10, null=True, unique=True)

    REQUIRED_FIELDS = []


class IdentificationNumber(models.Model):
    number = models.CharField(max_length=13, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('confirmed', 'Confirmed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    donator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donators')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation from {self.user.username}: {self.amount} ({self.status})"
