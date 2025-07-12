from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
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
        return JsonResponse(
            {'userName': username, 'error': 'Already Registered'}, status=409
        )

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


def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        print("DEBUG: raw reviews =", reviews, dealer_id)

        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail['review'])
            print(sentiment)
            review_detail['sentiment'] = sentiment['sentiment']

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    print("DEBUG: Post review", request.user)

    try:
        data = json.loads(request.body)
        response = post_review(data)
        print("DEBUG: Post review response", response)
        return JsonResponse({"status": 200})
    except Exception as e:
        print("Network exception occurred:", str(e))
        return JsonResponse({
            "status": 401,
            "message": "Error in posting review"
        })
