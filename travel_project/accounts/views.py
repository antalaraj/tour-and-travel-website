from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import AdminData
from .models import TravelGuide
from .forms import TravelGuideForm

from .models import Destination
from .forms import DestinationForm

from .models import UserProfile
from .forms import UserProfileForm, UserEditForm
from django.contrib.auth.decorators import login_required


from .models import TopDestination
from .forms import TopDestinationForm

from .models import Review
from .forms import ReviewForm

from .models import Blog
from .forms import BlogForm

from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Booking, BookingNotification, BookingStatus, PaymentStatus
from .forms import BookingForm, BookingStatusForm, PaymentForm
from django.db.models import Count, Q, Avg
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    if request.user.is_superuser:  # Check if the user is an admin
        user_type = "Admin"
    else:
        user_type = "Regular User"
    
    return render(request, 'userdata.html', {'user_type': user_type})

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/register.html')
            
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/register.html')
        
        try:
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                phone=phone,
                img=request.FILES.get('img')
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
            return render(request, 'accounts/register.html')
            
    return render(request, 'accounts/register.html')

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'accounts/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'accounts/login.html')
            
    return render(request, 'accounts/login.html')

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page


# Standard views
def index(request):
    travels = TravelGuide.objects.all()
    destinations = Destination.objects.all()
    topdestinations = TopDestination.objects.all().order_by('-created_at')
    
    # Get all blogs ordered by latest
    blogs = Blog.objects.order_by('-created_at')

    # Get the latest 3 blogs
    latest_blogs = blogs[:3]

    # Get featured reviews (reviews with is_featured=True)
    featured_reviews = Review.objects.filter(is_featured=True).select_related('user').order_by('-created_at')[:4]
    
    # If no featured reviews, get the latest reviews
    if not featured_reviews:
        featured_reviews = Review.objects.select_related('user').order_by('-created_at')[:4]

    return render(request, 'index.html', {
        'travels': travels,
        'destinations': destinations,
        'topdestinations': topdestinations,
        'latest_blogs': latest_blogs,
        'featured_reviews': featured_reviews,
    })

def about(request):
    travels = TravelGuide.objects.all()
    return render(request, 'about.html', {'travels': travels})


def blog(request):
    blogs = Blog.objects.order_by('-created_at')  # Fetch blogs ordered by newest first
    paginator = Paginator(blogs, 4)  # Show 4 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page

    latest_blogs = list(paginator.object_list[:3])  # Get latest 3 blogs

    return render(request, 'blog.html', {
        'latest_blogs': latest_blogs,
        'page_obj': page_obj,  # Use `page_obj` instead of `blogs` for pagination
    })

def blogs_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blogs_detail.html', {'blog': blog})
                  


def destination(request):
    topdestinations = TopDestination.objects.all()
    return render(request, 'destination.html', {'topdestinations': topdestinations})

def guide(request):
    travels = TravelGuide.objects.all()
    return render(request, 'guide.html', {'travels': travels})

def package(request):
    destinations = Destination.objects.all()
    topdestinations = TopDestination.objects.all()
    return render(request, 'package.html', {'destinations': destinations,
                                            'topdestinations': topdestinations})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    travel_guides = TravelGuide.objects.all()
    return render(request, 'destination_detail.html', {
        'destination': destination,
        'travel_guides': travel_guides
    })

def service(request):
    # Get featured reviews (reviews with is_featured=True)
    featured_reviews = Review.objects.filter(is_featured=True).select_related('user').order_by('-created_at')[:4]
    
    # If no featured reviews, get the latest reviews
    if not featured_reviews:
        featured_reviews = Review.objects.select_related('user').order_by('-created_at')[:4]

    return render(request, 'service.html', {
        'featured_reviews': featured_reviews,
    })

def single(request):
    return render(request, 'single.html')

def testimonial(request):
    # Get featured reviews (reviews with is_featured=True)
    featured_reviews = Review.objects.filter(is_featured=True).select_related('user').order_by('-created_at')[:4]
    
    # If no featured reviews, get the latest reviews
    if not featured_reviews:
        featured_reviews = Review.objects.select_related('user').order_by('-created_at')[:4]

    return render(request, 'testimonial.html', {
        'featured_reviews': featured_reviews,
    })

def admin_view(request):
    # Get today's bookings count
    today = datetime.now().date()
    today_bookings_count = Booking.objects.filter(created_at__date=today).count()
    
    # Get total users count
    total_users = User.objects.count()
    
    # Calculate average rating
    reviews = Review.objects.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get new messages count (all unread messages)
    new_messages_count = Contact.objects.count()
    
    # Get recent bookings
    recent_bookings = Booking.objects.select_related('user', 'package').order_by('-created_at')[:5]
    
    # Get popular destinations
    popular_destinations = Destination.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]
    
    # Get recent reviews
    recent_reviews = Review.objects.select_related('user').order_by('-created_at')[:5]
    
    context = {
        'today_bookings_count': today_bookings_count,
        'total_users': total_users,
        'average_rating': average_rating,
        'new_messages_count': new_messages_count,
        'recent_bookings': recent_bookings,
        'popular_destinations': popular_destinations,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'admin/index.html', context)

def create_missing_profiles():
    from django.contrib.auth.models import User
    from .models import UserProfile
    
    # Get all users without profiles
    users_without_profiles = User.objects.filter(userprofile=None)
    
    # Create profiles for users that don't have them
    for user in users_without_profiles:
        UserProfile.objects.create(user=user)
    
    return len(users_without_profiles)

def userdata(request):
    # First, ensure all users have profiles
    profiles_created = create_missing_profiles()
    if profiles_created > 0:
        print(f"Created {profiles_created} missing user profiles")
    
    users = UserProfile.objects.select_related('user').all()
    print("Number of users found:", users.count())
    return render(request, 'admin/userdata.html', {'users': users})

def update_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('userdata')
    else:
        form = UserEditForm(instance=user_profile)
    return render(request, 'admin/user_form.html', {'form': form, 'user': user_profile})

def delete_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    # Get the associated User instance
    user = user_profile.user
    # Delete the User (this will cascade delete the UserProfile)
    if user:
        user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('userdata')

# List all destinations
def formadmin(request):
    travels = TravelGuide.objects.all()
    return render(request, 'admin/form.html', {'travels': travels})

# View destination details

def travel_detail(request, pk):
    travel = get_object_or_404(TravelGuide, pk=pk)
    return render(request, 'admin/form.html', {'travel': travel})

# Create a new destination
def travel_create(request):
    if request.method == "POST":
        form = TravelGuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('formadmin')
    else:
        form = TravelGuideForm()
    return render(request, 'admin/travel_form.html', {'form': form})

# Update an existing destination
def travel_update(request, pk):
    travel = get_object_or_404(TravelGuide, pk=pk)
    if request.method == "POST":
        form = TravelGuideForm(request.POST, request.FILES, instance=travel)
        if form.is_valid():
            form.save()
            return redirect('formadmin')
    else:
        form = TravelGuideForm(instance=travel)
    return render(request, 'admin/travel_form.html', {'form': form})

# Delete a destination
def travel_delete(request, pk):
    travel = get_object_or_404(TravelGuide, pk=pk)
    if request.method == "POST":
        travel.delete()
        return redirect('formadmin')
    return render(request, 'admin/travel_confirm_delete.html', {'travel': travel})

# Read (List all destinations)
def packagelist(request):
    destinations = Destination.objects.all()
    return render(request, 'admin/packagelist.html', {'destinations': destinations})

# Create a new destination
def packagecreate(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('packagelist')
    else:
        form = DestinationForm()
    return render(request, 'admin/packageform.html', {'form': form})

# Update an existing destination
def packageupdate(request, id):
    destination = get_object_or_404(Destination, id=id)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('packagelist')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'admin/packageform.html', {'form': form})

# Delete a destination
def packagedelete(request, id):
    destination = get_object_or_404(Destination, id=id)
    if request.method == "POST":
        destination.delete()
        return redirect('packagelist')
    return render(request, 'admin/packagedelete.html', {'destination': destination})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm



def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact_create")  # Redirect to prevent form resubmission
        else:
            messages.error(request, "There was an error in your form. Please check and try again.")
    else:
        form = ContactForm()
    
    return render(request, "contact.html", {"form": form})

# Read (List Contacts)
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin/contact_list.html', {'contacts': contacts})

# Update (Edit Contact)
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Redirect to contact list after update
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contact.html', {'form': form})

# Delete (Remove Contact)
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect('contact_list')  # Redirect to contact list after deletion
    return render(request, 'admin/contact_confirm_delete.html', {'contact': contact})


# List all top destinations
def destination_list(request):
    topdestinations = TopDestination.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(topdestinations, 10)  # Show 10 destinations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/destinationlist.html', {
        'topdestinations': page_obj,
        'page_obj': page_obj
    })

# Create a new top destination
def destination_create(request):
    if request.method == 'POST':
        form = TopDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save()
            messages.success(request, f'Destination "{destination.title}" was created successfully.')
            return redirect('destinationlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TopDestinationForm()
    
    return render(request, 'admin/destinationform.html', {'form': form})

# Update a top destination
def destination_update(request, pk):
    destination = get_object_or_404(TopDestination, pk=pk)
    if request.method == 'POST':
        form = TopDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            destination = form.save()
            messages.success(request, f'Destination "{destination.title}" was updated successfully.')
            return redirect('destinationlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TopDestinationForm(instance=destination)
    
    return render(request, 'admin/destinationform.html', {'form': form})

# Delete a top destination
@require_POST
def destination_delete(request, pk):
    destination = get_object_or_404(TopDestination, pk=pk)
    try:
        destination.delete()
        messages.success(request, f'Destination "{destination.title}" was deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting destination: {str(e)}')
    
    return redirect('destinationlist')

# AJAX endpoint for tag suggestions
def get_tag_suggestions(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        # Get unique tags from existing destinations
        tags = set()
        for destination in TopDestination.objects.all():
            tags.update(destination.tags)
        
        # Filter tags based on query
        suggestions = [tag for tag in tags if query.lower() in tag.lower()]
        return JsonResponse({'results': suggestions})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# List all reviews
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'admin/review_list.html', {'reviews': reviews})

# Create a new review
@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.POST.get('user')  # Set the user from the form
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    users = User.objects.all()
    return render(request, 'admin/review_form.html', {'form': form, 'users': users})

# Update an existing review
@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.POST.get('user')  # Update the user from the form
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    users = User.objects.all()
    return render(request, 'admin/review_form.html', {'form': form, 'users': users})

# Delete a review
@login_required
def review_delete(request, pk):
    if request.user.is_staff:
        review = get_object_or_404(Review, pk=pk)
    else:
        review = get_object_or_404(Review, pk=pk, user=request.user)
    
    if request.method == "POST":
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('review_list')
    return render(request, 'admin/review_confirm_delete.html', {'review': review})



@login_required
def package_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.package = destination
            booking.user = request.user
            # Calculate total amount based on number of travelers
            booking.total_amount = destination.price * form.cleaned_data['travelers']
            
            # Handle travel guide selection
            travel_guide_id = request.POST.get('travel_guide')
            if travel_guide_id:
                travel_guide = get_object_or_404(TravelGuide, id=travel_guide_id)
                destination.travel_guide = travel_guide
                destination.save()
            
            booking.save()
            
            # Create notification
            BookingNotification.objects.create(
                booking=booking,
                message=f"New booking request for {destination.name}"
            )
            
            messages.success(request, 'Your booking request has been submitted successfully!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'accounts/package_detail.html', {
        'destination': destination,
        'form': form,
        'travel_guides': TravelGuide.objects.all()
    })

# View all blogs
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'admin/blog_list.html', {'blogs': blogs})

# View single blog
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'admin/blog_detail.html', {'blog': blog})

# Create a new blog
@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'admin/blog_form.html', {'form': form})

# Update an existing blog
@login_required
def blog_update(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin/blog_form.html', {'form': form})

# Delete a blog
@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('blog_list')

def admin_booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'admin/booking_list.html', {'bookings': bookings})

def topdestination_detail(request, pk):
    destination = get_object_or_404(TopDestination, pk=pk)
    return render(request, 'topdestination_detail.html', {
        'destination': destination
    })

@login_required
def payment(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination_id')
        travel_date = request.POST.get('travel_date')
        travelers = request.POST.get('travelers')
        travel_guide_id = request.POST.get('travel_guide')
        special_requests = request.POST.get('special_requests', '')
        payment_method = request.POST.get('payment_method', 'online')

        try:
            destination = Destination.objects.get(id=destination_id)
            travel_guide = TravelGuide.objects.get(id=travel_guide_id)
            total_amount = float(destination.price) * int(travelers)

            if payment_method == 'online':
                # Simulate online payment processing
                payment_status = PaymentStatus.COMPLETED
                booking_status = BookingStatus.CONFIRMED
            else:
                # COD payment
                payment_status = PaymentStatus.PENDING
                booking_status = BookingStatus.PENDING

            # Create the booking
            booking = Booking.objects.create(
                package=destination,
                user=request.user,
                travel_date=travel_date,
                travelers=travelers,
                total_amount=total_amount,
                payment_status=payment_status,
                status=booking_status,
                special_requests=special_requests
            )

            # Create notification
            BookingNotification.objects.create(
                booking=booking,
                message=f"Your booking for {destination.name} has been confirmed. Payment status: {payment_status}."
            )

            # Send success message
            if payment_method == 'online':
                messages.success(request, 'Payment successful! Your booking has been confirmed.')
            else:
                messages.success(request, 'Booking confirmed! Please complete the payment on delivery.')

            # Redirect to my-bookings page
            return redirect('bookings:my_bookings')

        except (Destination.DoesNotExist, TravelGuide.DoesNotExist):
            messages.error(request, 'Invalid destination or travel guide selected.')
            return redirect('destination_detail', pk=destination_id)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('destination_detail', pk=destination_id)

    # GET request - show payment form
    try:
        destination_id = request.GET.get('destination_id')
        travel_date = request.GET.get('travel_date')
        travelers = request.GET.get('travelers')
        travel_guide_id = request.GET.get('travel_guide')
        special_requests = request.GET.get('special_requests', '')

        if not all([destination_id, travel_date, travelers, travel_guide_id]):
            messages.error(request, 'Missing required booking information.')
            return redirect('index')

        destination = Destination.objects.get(id=destination_id)
        travel_guide = TravelGuide.objects.get(id=travel_guide_id)
        total_amount = float(destination.price) * int(travelers)

        context = {
            'destination': destination,
            'travel_date': travel_date,
            'travelers': travelers,
            'travel_guide': travel_guide,
            'total_amount': total_amount,
            'special_requests': special_requests
        }
        return render(request, 'payment.html', context)

    except (Destination.DoesNotExist, TravelGuide.DoesNotExist):
        messages.error(request, 'Invalid destination or travel guide selected.')
        return redirect('index')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('index')


