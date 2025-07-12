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

    # Dealer-related paths
    path(
        'get_dealers/',
        views.get_dealerships,
        name='get_dealers'
    ),
    path(
        'get_dealers/<str:state>',
        views.get_dealerships,
        name='get_dealers_by_state'
    ),
    path(
        'dealer/<int:dealer_id>',
        views.get_dealer_details,
        name='dealer_details'
    ),
    path(
        'reviews/dealer/<int:dealer_id>',
        views.get_dealer_reviews,
        name='dealer_reviews'
    ),
    path('add_review', views.add_review, name='add_review'),
]

# Serve media files during development
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
