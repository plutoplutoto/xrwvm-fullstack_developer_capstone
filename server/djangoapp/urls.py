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
    # path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path('djangoapp/get_dealers/', views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    # path('dealer/<int:dealer_id>/reviews', views.get_dealer_reviews, name='dealer_reviews'),
    # path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    # path('add_review', views.add_review, name='add_review'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
