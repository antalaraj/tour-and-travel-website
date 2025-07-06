from django import forms
from accounts.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travelers', 'travel_date', 'special_requests']

    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        self.fields['travel_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['travelers'].widget = forms.NumberInput(attrs={'min': 1})
        self.fields['special_requests'].widget = forms.Textarea(attrs={'rows': 3}) 