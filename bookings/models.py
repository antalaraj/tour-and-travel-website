from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

class TravelPackage(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.CharField(max_length=100)  # e.g., "7 days", "2 weeks"
    available_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    number_of_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.package.name}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.package.price * self.number_of_people
        super().save(*args, **kwargs)

class TopDestinationBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topdestination = models.ForeignKey('accounts.TopDestination', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    number_of_people = models.PositiveIntegerField(default=1)
    travel_date = models.DateField()
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.topdestination.title}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.topdestination.price * self.number_of_people
        super().save(*args, **kwargs)
