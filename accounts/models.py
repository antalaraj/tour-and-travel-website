# Create your models here.
from django.contrib.auth.models import User
from django import forms


from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.username if self.user else "No user"

class AdminData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class TravelGuide(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/img/', blank=True, null=True)

    def __str__(self):
        return self.name



class Destination(models.Model):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    persons = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='static/img/')
    trip_roadmap = models.TextField(blank=True, null=True, help_text="Detailed trip itinerary and planning roadmap")

    def __str__(self):
        return self.name



class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Orders contacts by newest first

    def __str__(self):
        return f"{self.name} - {self.subject}"  # More informative string representation


    
class TopDestination(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=255)
    img = models.ImageField(upload_to='top_destinations/', null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    tags = models.JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        # If title is not set, use location as title
        if not self.title:
            self.title = self.location
        # Ensure tags is always a list
        if isinstance(self.tags, str):
            self.tags = [self.tags]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.location


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    customer_image = models.ImageField(upload_to='review_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"

    def get_customer_name(self):
        return self.user.get_full_name() or self.user.username


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    REFUNDED = 'refunded', 'Refunded'
    FAILED = 'failed', 'Failed'

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    travelers = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    travel_guide = models.ForeignKey(TravelGuide, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'payment_status']),
            models.Index(fields=['travel_date']),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.package.name}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.package.price * self.travelers
        super().save(*args, **kwargs)

    def get_travel_guide(self):
        return self.travel_guide or self.package.travel_guide

class BookingNotification(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for Booking {self.booking.id}"

class TopDestinationBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destination = models.ForeignKey(TopDestination, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='top_destination_bookings')
    booking_date = models.DateTimeField(default=timezone.now)
    travel_date = models.DateField()
    travelers = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'payment_status']),
            models.Index(fields=['travel_date']),
        ]

    def __str__(self):
        return f"Top Destination Booking {self.id} - {self.destination.title}"
