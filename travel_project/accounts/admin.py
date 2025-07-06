from django.contrib import admin
from .models import AdminData
from .models import UserProfile
from .models import Destination
from .models import TopDestination
from .models import Review
from .models import Contact
from .models import Blog

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

admin.site.register(Destination)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')


@admin.register(TopDestination)
class TopDestinationAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'rating', 'created_at']
    search_fields = ['title', 'location', 'description']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at', 'updated_at']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'created_at')
    search_fields = ('user__username', 'rating')
    list_filter = ('rating', 'created_at')



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')


