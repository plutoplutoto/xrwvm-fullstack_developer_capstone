from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for user registration
    path('register', views.registration, name='registration'),

    # Paths for login and logout
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # Path to retrieve car data
    path('get_cars', views.get_cars, name='getcars'),

    # Add more paths like:
    # path('dealer/<int:dealer_id>/reviews', views.get_dealer_reviews, name='dealer_reviews'),
    # path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    # path('add_review', views.add_review, name='add_review'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
