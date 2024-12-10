# from django.shortcuts import render
# from .models import Restaurant
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from datetime import datetime
# from django.db.models import Q
# from math import radians, cos, sin, sqrt
# import logging

# logger = logging.getLogger(__name__)

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0  
#     lat1_rad = radians(lat1)
#     lon1_rad = radians(lon1)
#     lat2_rad = radians(lat2)
#     lon2_rad = radians(lon2)

#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
#     c = 2 * sin(sqrt(a))

#     return R * c 

# class RestaurantQueryView(APIView):
#     def get(self, request):
#         try:
#             user_lat = float(request.query_params.get('latitude'))
#             user_lon = float(request.query_params.get('longitude'))

#             if not (-90 <= user_lat <= 90) or not (-180 <= user_lon <= 180):
#                 logger.error("Invalid coordinates received.")
#                 return Response({"error": "Invalid latitude or longitude."}, status=status.HTTP_400_BAD_REQUEST)

#             current_time = datetime.now().time()

#             logger.info(f"Received user location: Latitude: {user_lat}, Longitude: {user_lon}")

#             restaurants = Restaurant.objects.exclude(
#                 Q(latitude__isnull=True) | Q(longitude__isnull=True)
#             ).filter(
#                 open_hour__lte=current_time,
#                 close_hour__gte=current_time
#             )
#             # print(restaurants[::5])

#             if not restaurants.exists():
#                 logger.info("No restaurants found with valid operational hours and coordinates.")
#                 return Response({"restaurants": []}, status=status.HTTP_200_OK)

#             nearby_restaurants = []

#             for restaurant in restaurants:
#                 distance = haversine(user_lat, user_lon, restaurant.latitude, restaurant.longitude)
#                 logger.info(f"Restaurant ID: {restaurant.id} is {distance} km away.")

#                 if distance <= restaurant.availability_radius:
#                     nearby_restaurants.append(restaurant.id)

#             return Response({"restaurants": nearby_restaurants}, status=status.HTTP_200_OK)

#         except Exception as e:
#             logger.error(f"Error occurred: {str(e)}")
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Q
from math import radians, sin, cos, sqrt
from .models import Restaurant
from .paginator import RestaurantPagination  
import logging

logger = logging.getLogger(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * sin(sqrt(a))

    return R * c  

class RestaurantQueryView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get('latitude'))
            user_lon = float(request.query_params.get('longitude'))

            if not (-90 <= user_lat <= 90) or not (-180 <= user_lon <= 180):
                logger.error("Invalid coordinates received.")
                return Response({"error": "Invalid latitude or longitude."}, status=status.HTTP_400_BAD_REQUEST)

            current_time = datetime.now().time()

            logger.info(f"Received user location: Latitude: {user_lat}, Longitude: {user_lon}")
            restaurants = Restaurant.objects.exclude(
                Q(latitude__isnull=True) | Q(longitude__isnull=True)
            ).filter(
                open_hour__lte=current_time,
                close_hour__gte=current_time
            )

            nearby_restaurants = []

            for restaurant in restaurants:
                distance = haversine(user_lat, user_lon, restaurant.latitude, restaurant.longitude)
              
                if float(distance) <= restaurant.availability_radius:
                    nearby_restaurants.append({
                        "id": restaurant.id,
                        "latitude": restaurant.latitude,
                        "longitude": restaurant.longitude,
                        "distance": distance,  
                    })

            paginator = RestaurantPagination()
            page_obj = paginator.paginate_queryset(nearby_restaurants, request)

            return paginator.get_paginated_response({
                "restaurants": page_obj
            })

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
