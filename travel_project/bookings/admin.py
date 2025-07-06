from django.contrib import admin
from .models import TravelPackage, Booking, TopDestinationBooking

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'available_seats', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'status', 'number_of_people', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'package__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TopDestinationBooking)
class TopDestinationBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topdestination', 'status', 'number_of_people', 'travel_date', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'topdestination__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
