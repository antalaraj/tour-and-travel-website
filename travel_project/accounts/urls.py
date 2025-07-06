from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
     path('', views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('index', views.index, name='index'),
    path("about/", views.about, name="about"),
    path('blog', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blogs_detail, name='blogs_detail'),
    path('destination', views.destination, name='destination'),
    path('guide', views.guide, name='guide'),
    path('package', views.package, name='package'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('topdestination/<int:pk>/', views.topdestination_detail, name='topdestination_detail'),
    path('service', views.service, name='service'),
    path('single', views.single, name='single'),
    path('testimonial', views.testimonial, name='testimonial'),
    path('admin',views.admin_view,name='admin'),
    path('formadmin',views.formadmin,name='formadmin'),


    path('<int:pk>/', views.travel_detail, name='travel_detail'),
    path('new/', views.travel_create, name='travel_create'),
    path('<int:pk>/edit/', views.travel_update, name='travel_update'),
    path('<int:pk>/delete/', views.travel_delete, name='travel_delete'),

    path('packagelist', views.packagelist, name='packagelist'),
    path('create/', views.packagecreate, name='packagecreate'),
    path('<int:id>/update/', views.packageupdate, name='packageupdate'),
    path('<int:id>/deletee/', views.packagedelete, name='packagedelete'),

    path('users/', views.userdata, name='userdata'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
   
    path('contact/', views.contact_create, name='contact_create'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contact/edit/<int:pk>/', views.contact_update, name='contact_update'),
    path('contact/delete/<int:pk>/', views.contact_delete, name='contact_delete'),

    path('destinationlist', views.destination_list, name='destinationlist'),
    path('destinationcreate/', views.destination_create, name='destinationcreate'),
    path('destination/<int:pk>/delete/', views.destination_delete, name='destinationdelete'),
    path('<int:pk>/edite/', views.destination_update, name='destinationupdate'),
    path('destination/tag-suggestions/', views.get_tag_suggestions, name='tag_suggestions'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/new/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/<int:blog_id>/update/', views.blog_update, name='blog_update'),
    path('blogs/<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('payment/', views.payment, name='payment'),

  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    