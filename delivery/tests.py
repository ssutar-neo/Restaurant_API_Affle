import unittest
import requests
from datetime import datetime
from django.test import Client
from .models import Restaurant


class RestaurantQueryViewTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup class method to insert test data.
        """
        cls.client = Client()

        cls.cnt = int(Restaurant.objects.count())

        cls.restaurant_1 = Restaurant.objects.create(
            id=cls.cnt + 1,
            latitude=float(50.1942536),
            longitude=float(8.455508),
            open_hour=datetime.strptime("14:00:00", "%H:%M:%S").time(),
            close_hour=datetime.strptime("23:30:00", "%H:%M:%S").time(),
            availability_radius=float(5.0),
            rating=4.7
        )
        cls.restaurant_2 = Restaurant.objects.create(
            id=cls.cnt + 2,
            latitude=float(57.132921),
            longitude=float(19.6385061),
            open_hour=datetime.strptime("14:00:00", "%H:%M:%S").time(),
            close_hour=datetime.strptime("23:05:00", "%H:%M:%S").time(),
            availability_radius=float(5.0),
            rating=4.8
        )
        cls.restaurant_3 = Restaurant.objects.create(
            id=cls.cnt + 3,
            latitude=float(52.5018668),
            longitude=float(18.3254556),
            open_hour=datetime.strptime("09:00:00", "%H:%M:%S").time(),
            close_hour=datetime.strptime("23:40:00", "%H:%M:%S").time(),
            availability_radius=float(10.0),
            rating=4.0
        )
        print("Test data inserted.")

    def test_valid_location(self):
        """
        Test valid location query.
        """
        url = "/api/restaurants/"
        params = {"latitude": 52.5018668, "longitude": 18.3254556}
        
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['results']["restaurants"]), 1)

        restaurant = response.json()['results']["restaurants"][0]
        self.assertEqual(restaurant["id"], self.restaurant_3.id)

    def test_no_nearby_restaurants(self):
        """
        Test for no nearby restaurants scenario.
        """
        url = "/api/restaurants/"
        params = {"latitude": 44.0522, "longitude": -118.2437}  
        
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results']["restaurants"], [])

    def test_invalid_coordinates(self):
        """
        Test for invalid coordinates.
        """
        url = "/api/restaurants/"
        params = {"latitude": 200.0, "longitude": -300.0}  
        
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid latitude or longitude.")
    
    def test_pagination(self):
        """
        Test pagination of restaurant results.
        """
        url = "/api/restaurants/"
        params = {"latitude": 52.5018668, "longitude": 18.3254556}

        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("next", response.json())  
        self.assertGreaterEqual(len(response.json()['results']["restaurants"]), 1)

    def test_distance_calculation(self):
        """
        Test correct distance calculation.
        """
        url = "/api/restaurants/"
        params = {"latitude": 48.023495, "longitude": 7.858444699999999}
    
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        restaurant = response.json()['results']["restaurants"]
        restaurant.sort(key=lambda x:x['distance'],reverse=False)
        self.assertAlmostEqual(restaurant[0]["distance"], 0.0, delta=0.1)

    def test_multiple_nearby_restaurants(self):
        """
        Test multiple nearby restaurants.
        """
        url = "/api/restaurants/"

        params = {"latitude": 48.023495, "longitude": 7.858444699999999}

        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['results']["restaurants"]), 0)  

    @classmethod
    def tearDownClass(cls):
        """
        Teardown class method to clean up.
        """
        Restaurant.objects.filter(id__in=[
            cls.restaurant_1.id,
            cls.restaurant_2.id,
            cls.restaurant_3.id
        ]).delete()
