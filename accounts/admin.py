from django.contrib import admin
from .models import AdminData
from .models import UserProfile
from .models import Destination
from .models import TopDestination
from .models import Review
from .models import Contact
from .models import Blog
from .models import Booking, TravelGuide, BookingNotification, TopDestinationBooking

admin.site.register(AdminData)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'get_last_name', 'get_email', 'get_password', 'phone', 'img', 'get_date_joined', 'get_last_login')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('user__is_active', 'user__is_staff', 'user__is_superuser')
    readonly_fields = ('get_password', 'get_date_joined', 'get_last_login')

    def get_username(self, obj):
        return obj.user.username if obj.user else "No user"
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "No first name"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "No last name"
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email if obj.user else "No email"
    get_email.short_description = 'Email'

    def get_password(self, obj):
        return "********" if obj.user else "No password"
    get_password.short_description = 'Password'

    def get_date_joined(self, obj):
        return obj.user.date_joined if obj.user else "No date"
    get_date_joined.short_description = 'Date Joined'

    def get_last_login(self, obj):
        return obj.user.last_login if obj.user else "Never"
    get_last_login.short_description = 'Last Login'

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)
        return [
            ('User Information', {
                'fields': ('user', 'get_username', 'get_first_name', 'get_last_name', 'get_email', 'get_password')
            }),
            ('Profile Information', {
                'fields': ('img', 'phone')
            }),
            ('Account Information', {
                'fields': ('get_date_joined', 'get_last_login'),
                'classes': ('collapse',)
            })
        ]

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'persons', 'price')
    search_fields = ('name', 'description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'package', 'user', 'travel_date', 'travelers', 'total_amount', 'status', 'payment_status', 'travel_guide')
    list_filter = ('status', 'payment_status', 'travel_guide')
    search_fields = ('id', 'package__name', 'user__username', 'travel_guide__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'package', 'user', 'travel_date', 'travelers', 'total_amount')
        }),
        ('Travel Guide', {
            'fields': ('travel_guide',)
        }),
        ('Status Information', {
            'fields': ('status', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('package', 'user', 'travel_guide')

@admin.register(TravelGuide)
class TravelGuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'image')
    search_fields = ('name', 'designation')

@admin.register(BookingNotification)
class BookingNotificationAdmin(admin.ModelAdmin):
    list_display = ('booking', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('booking__id', 'message')

@admin.register(TopDestination)
class TopDestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('title', 'location', 'description')

@admin.register(TopDestinationBooking)
class TopDestinationBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination', 'user', 'travel_date', 'travelers', 'total_amount', 'status', 'payment_status')
    list_filter = ('status', 'payment_status')
    search_fields = ('id', 'destination__title', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'created_at')
    search_fields = ('user__username', 'rating')
    list_filter = ('rating', 'created_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')


