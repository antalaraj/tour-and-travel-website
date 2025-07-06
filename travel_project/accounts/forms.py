from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TravelGuide
from .models import AdminData
from .models import Destination
from django.core.exceptions import ValidationError
from .models import UserProfile
from .models import TopDestination
from .models import Review
from django import forms
from .models import Contact
from .models import Blog
from .models import Booking, BookingStatus, PaymentStatus
from django.utils import timezone
from datetime import timedelta



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['img', 'phone']


class AdminDataForm(forms.ModelForm):
    class Meta:
        model = AdminData
        fields = ['name', 'email']


class TravelGuideForm(forms.ModelForm):
    class Meta:
        model = TravelGuide
        fields = ['name', 'designation', 'image']


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'duration', 'persons', 'description', 'rating', 'price', 'img', 'trip_roadmap']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '5', 'step': '0.1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'persons': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'trip_roadmap': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Enter detailed day-by-day itinerary and planning roadmap...',
                'style': 'resize: vertical;'
            })
        }
        help_texts = {
            'trip_roadmap': 'Provide a detailed day-by-day itinerary and planning roadmap for the trip.'
        }




class TopDestinationForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)

    class Meta:
        model = TopDestination
        fields = ['title', 'description', 'location', 'img', 'rating', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'maxlength': '500'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 500:
            raise forms.ValidationError("Description cannot exceed 500 characters.")
        return description

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not 1 <= rating <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            return [tags]
        return []



class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.Select(
            choices=[(i, '★' * i) for i in range(1, 6)],
            attrs={'class': 'form-select'}
        )
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}
        )
    )
    customer_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment', 'customer_image']




class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']


class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'img']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if user_profile.user:
            user_profile.user.username = self.cleaned_data['username']
            user_profile.user.email = self.cleaned_data['email']
            if commit:
                user_profile.user.save()
                user_profile.save()
        return user_profile


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_date', 'travelers', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date', 'min': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_travel_date(self):
        travel_date = self.cleaned_data.get('travel_date')
        if travel_date < timezone.now().date():
            raise ValidationError("Travel date cannot be in the past")
        return travel_date

    def clean_travelers(self):
        travelers = self.cleaned_data.get('travelers')
        if travelers < 1:
            raise ValidationError("Number of travelers must be at least 1")
        return travelers


class BookingStatusForm(forms.Form):
    status = forms.ChoiceField(choices=BookingStatus.choices)
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
    ])


