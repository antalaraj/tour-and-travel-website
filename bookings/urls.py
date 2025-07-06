from django.urls import path
from . import views
from .views import (
    PackageListView, PackageDetailView, BookingCreateView, MyBookingsView,
    AdminBookingListView, admin_booking_update, BookingDeleteView, UserBookingDeleteView,
    TopDestinationDetailView, TopDestinationBookingCreateView, MyTopDestinationBookingsView,
    AdminTopDestinationBookingListView, admin_topdestination_booking_update,
    TopDestinationBookingDeleteView, UserTopDestinationBookingDeleteView
)

app_name = 'bookings'

urlpatterns = [
    path('', views.PackageListView.as_view(), name='package_list'),
    path('package/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('package/<int:pk>/book/', views.BookingCreateView.as_view(), name='create_booking'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('my-bookings/<uuid:pk>/delete/', views.UserBookingDeleteView.as_view(), name='user_booking_delete'),
    path('admin/bookings/', views.AdminBookingListView.as_view(), name='admin_booking_list'),
    path('admin/bookings/<uuid:pk>/update/', views.admin_booking_update, name='admin_booking_update'),
    path('admin/bookings/<uuid:pk>/delete/', views.BookingDeleteView.as_view(), name='admin_booking_delete'),
    path('topdestination/<int:pk>/', TopDestinationDetailView.as_view(), name='topdestination_detail'),
    path('topdestination/<int:pk>/book/', TopDestinationBookingCreateView.as_view(), name='create_topdestination_booking'),
    path('my-topdestination-bookings/', MyTopDestinationBookingsView.as_view(), name='my_topdestination_bookings'),
    path('admin/topdestination-bookings/', AdminTopDestinationBookingListView.as_view(), name='admin_topdestination_booking_list'),
    path('admin/topdestination-bookings/<uuid:pk>/update/', admin_topdestination_booking_update, name='admin_topdestination_booking_update'),
    path('admin/topdestination-bookings/<uuid:pk>/delete/', TopDestinationBookingDeleteView.as_view(), name='admin_topdestination_booking_delete'),
    path('my-topdestination-bookings/<uuid:pk>/delete/', UserTopDestinationBookingDeleteView.as_view(), name='user_topdestination_booking_delete'),
    path('payment/<int:destination_id>/', views.payment, name='payment'),
    path('confirm-booking/<int:destination_id>/', views.confirm_booking, name='confirm_booking'),
] 