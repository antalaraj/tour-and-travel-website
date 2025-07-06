from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from accounts.models import Booking, Destination, BookingStatus, TravelGuide, PaymentStatus, TopDestination, TopDestinationBooking
from .forms import BookingForm
import uuid
from django.http import Http404

class PackageListView(ListView):
    model = Destination
    template_name = 'bookings/package_list.html'
    context_object_name = 'packages'

class PackageDetailView(DetailView):
    model = Destination
    template_name = 'bookings/package_detail.html'
    context_object_name = 'package'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:my_bookings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = get_object_or_404(Destination, pk=self.kwargs['pk'])
        context['travel_guides'] = TravelGuide.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['package'] = get_object_or_404(Destination, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        package = get_object_or_404(Destination, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.package = package
        
        # Get travelers from the form data
        travelers = int(self.request.POST.get('travelers', 1))
        form.instance.travelers = travelers
        
        # Calculate total amount
        total_amount = package.price * travelers
        form.instance.total_amount = total_amount
        
        # Set initial status
        form.instance.status = BookingStatus.PENDING
        form.instance.payment_status = PaymentStatus.PENDING
        
        # Handle travel guide selection
        travel_guide_id = self.request.POST.get('travel_guide')
        if travel_guide_id:
            try:
                travel_guide = get_object_or_404(TravelGuide, id=travel_guide_id)
                package.travel_guide = travel_guide
                package.save()
                messages.success(self.request, f'Travel guide {travel_guide.name} has been assigned to your booking.')
            except Exception as e:
                messages.warning(self.request, f'Error assigning travel guide: {str(e)}')
                return self.form_invalid(form)
        else:
            messages.warning(self.request, 'Please select a travel guide for your booking.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        messages.success(self.request, 'Your booking has been created successfully!')
        return response

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class AdminBookingListView(UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'bookings/admin_booking_list.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Booking.objects.select_related('package', 'package__travel_guide').all().order_by('-created_at')

@login_required
def admin_booking_update(request, pk):
    if not request.user.is_staff:
        return redirect('bookings:package_list')
    
    try:
        booking_uuid = uuid.UUID(str(pk))
        booking = get_object_or_404(Booking, id=booking_uuid)
    except ValueError:
        messages.error(request, 'Invalid booking ID')
        return redirect('bookings:admin_booking_list')
    
    if request.method == 'POST':
        # Get the new status values from the form
        new_status = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')
        
        # Update the booking status
        if new_status in dict(BookingStatus.choices):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking status updated to {booking.get_status_display()}')
        
        # Update the payment status
        if new_payment_status in dict(PaymentStatus.choices):
            booking.payment_status = new_payment_status
            booking.save()
            messages.success(request, f'Payment status updated to {booking.get_payment_status_display()}')
        
        return redirect('bookings:admin_booking_list')
    
    context = {
        'booking': booking,
        'status_choices': BookingStatus.choices,
        'payment_status_choices': PaymentStatus.choices
    }
    return render(request, 'bookings/admin_booking_update.html', context)

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:admin_booking_list')
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Booking has been deleted successfully.')
        return super().delete(request, *args, **kwargs)

class UserBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:my_bookings')
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your booking has been cancelled successfully.')
        return super().delete(request, *args, **kwargs)

class TopDestinationDetailView(DetailView):
    model = TopDestination
    template_name = 'accounts/topdestination_detail.html'
    context_object_name = 'topdestination'

class TopDestinationBookingCreateView(LoginRequiredMixin, CreateView):
    model = TopDestinationBooking
    fields = ['number_of_people', 'travel_date', 'special_requests']
    template_name = 'accounts/topdestination_detail.html'
    success_url = reverse_lazy('bookings:my_bookings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topdestination'] = get_object_or_404(TopDestination, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        topdestination = get_object_or_404(TopDestination, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.topdestination = topdestination
        form.instance.total_price = topdestination.price * form.instance.number_of_people
        
        response = super().form_valid(form)
        messages.success(self.request, 'Your booking has been created successfully!')
        return response

class MyTopDestinationBookingsView(LoginRequiredMixin, ListView):
    model = TopDestinationBooking
    template_name = 'bookings/my_topdestination_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return TopDestinationBooking.objects.filter(user=self.request.user)

class AdminTopDestinationBookingListView(UserPassesTestMixin, ListView):
    model = TopDestinationBooking
    template_name = 'bookings/admin_topdestination_booking_list.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return TopDestinationBooking.objects.select_related('topdestination').all().order_by('-created_at')

@login_required
def admin_topdestination_booking_update(request, pk):
    if not request.user.is_staff:
        return redirect('bookings:package_list')
    
    try:
        booking_uuid = uuid.UUID(str(pk))
        booking = get_object_or_404(TopDestinationBooking, id=booking_uuid)
    except ValueError:
        messages.error(request, 'Invalid booking ID')
        return redirect('bookings:admin_topdestination_booking_list')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            booking.status = 'approved'
            booking.save()
            messages.success(request, 'Booking has been approved successfully.')
        elif action == 'reject':
            booking.status = 'rejected'
            booking.save()
            messages.success(request, 'Booking has been rejected.')
        return redirect('bookings:admin_topdestination_booking_list')
    
    return render(request, 'bookings/admin_topdestination_booking_update.html', {'booking': booking})

class TopDestinationBookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TopDestinationBooking
    template_name = 'bookings/topdestination_booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:admin_topdestination_booking_list')
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Booking has been deleted successfully.')
        return super().delete(request, *args, **kwargs)

class UserTopDestinationBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = TopDestinationBooking
    template_name = 'bookings/topdestination_booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:my_topdestination_bookings')
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    
    def get_queryset(self):
        return TopDestinationBooking.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your booking has been cancelled successfully.')
        return super().delete(request, *args, **kwargs)

def payment(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    if request.method == 'POST':
        # Get form data
        travel_date = request.POST.get('travel_date')
        travelers = request.POST.get('travelers')
        travel_guide_id = request.POST.get('travel_guide')
        special_requests = request.POST.get('special_requests')
        
        # Get travel guide
        travel_guide = get_object_or_404(TravelGuide, id=travel_guide_id)
        
        # Calculate total amount
        total_amount = destination.price * int(travelers)
        
        context = {
            'destination': destination,
            'travel_date': travel_date,
            'travelers': travelers,
            'travel_guide': travel_guide,
            'special_requests': special_requests,
            'total_amount': total_amount,
        }
        return render(request, 'payment.html', context)
    
    return redirect('destinations:detail', destination_id=destination_id)

def confirm_booking(request, destination_id):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=destination_id)
        travel_date = request.POST.get('travel_date')
        travelers = request.POST.get('travelers')
        travel_guide_id = request.POST.get('travel_guide')
        special_requests = request.POST.get('special_requests')
        payment_method = request.POST.get('payment_method')
        
        # Calculate total amount
        total_amount = destination.price * int(travelers)
        
        # Create booking with pending status
        booking = Booking.objects.create(
            user=request.user,
            package=destination,
            travel_date=travel_date,
            travelers=travelers,
            total_amount=total_amount,
            special_requests=special_requests,
            status=BookingStatus.PENDING,  # Set initial status to pending
            payment_status='completed' if payment_method == 'online' else 'pending'
        )
        
        # Redirect to my bookings page
        messages.success(request, 'Booking request submitted successfully! Please wait for admin approval.')
        return redirect('bookings:my_bookings')
    
    return redirect('destinations:detail', destination_id=destination_id)
