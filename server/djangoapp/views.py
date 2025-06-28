from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt  # Optional: safer to use CSRF with frontend header
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import CarMake, CarModel
from .populate import initiate
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Replace with proper CSRF handling in production
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid input'}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'userName': username, 'status': 'Authenticated'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


@csrf_exempt
@require_POST
def registration(request):
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid input'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'userName': username, 'error': 'Already Registered'}, status=409)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    login(request, user)
    return JsonResponse({'userName': username, 'status': 'Authenticated'})


def logout_request(request):
    logout(request)
    return JsonResponse({'userName': ''})


# def get_cars(request):
#     if CarMake.objects.count() == 0:
#         initiate()

#     car_models = CarModel.objects.select_related('car_make')
#     cars = [
#         {"CarModel": cm.name, "CarMake": cm.car_make.name}
#         for cm in car_models
#     ]
#     return JsonResponse({"CarModels": cars})
def get_cars(request):
    if CarModel.objects.count() == 0:
        print("No car models found. Calling initiate() to populate...")
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    print(f"Car models found: {car_models.count()}")
    
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
