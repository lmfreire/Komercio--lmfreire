from itertools import product
from urllib import response
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from users.models import User
from products.models import Product

class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/products/"
        
        cls.product_1 = {
            "description": "Smartband xyz 3.0",
            "price": 100.99,
            "quantity": 15
        }

        cls.product_2 = {
            "description": "Smartband xyz 3.0",
            "price": 100.99,
            "quantity": 15
        }
        
        cls.user_seller_data_1 = {
            "username": "fre",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }
        
        cls.user_seller_data_2 = {
            "username": "erf",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }
        
        cls.user_normal_data = {
            "username": "luc",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": False
        }
        
        cls.user_adm_data = {
            "username": "math",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": False,
            "is_superuser": True
        }

        cls.user_login_seller_1 = {
            "username": "fre",
            "password": "abcd"
        }
        
        cls.user_login_seller_2 = {
            "username": "erf",
            "password": "abcd"
        }
        
        cls.user_login_normal = {
            "username": "luc",
            "password": "abcd"
        }

        cls.user_login_adm = {
            "username": "math",
            "password": "abcd"
        }
        
        cls.user_adm = User.objects.create_superuser(**cls.user_adm_data)
        cls.token_adm = Token.objects.create(user=cls.user_adm)
        
        cls.user_seller_1 = User.objects.create_superuser(**cls.user_seller_data_1)
        cls.token_seller_1 = Token.objects.create(user=cls.user_seller_1)
        
        cls.user_seller_2 = User.objects.create_superuser(**cls.user_seller_data_2)
        cls.token_seller_2 = Token.objects.create(user=cls.user_seller_2)
        
        cls.user_normal = User.objects.create_superuser(**cls.user_normal_data)
        cls.token_normal = Token.objects.create(user=cls.user_normal)
        
        cls.update_data = {
           "description": "Smartband XYZ 1000000"
        }
        
    def test_create_product_fail(self):
        response = self.client.post(self.url, self.product_1)
        
        expected = status.HTTP_401_UNAUTHORIZED
        result = response.status_code
        self.assertEqual(expected, result)
    
    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller_1.key)
        response = self.client.post(self.url, self.product_1)
        
        expected = status.HTTP_201_CREATED
        result = response.status_code
        self.assertEqual(expected, result)
        self.assertIn('id', response.data)
        self.assertIn("description",  response.data)

    def test_create_prduct_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_normal.key)
        response = self.client.post(self.url, self.product_1)
        
        expected = status.HTTP_403_FORBIDDEN
        result = response.status_code
        self.assertEqual(expected, result)
    
    def test_create_wrong_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller_1.key)

        response = self.client.post(self.url, data={})

        expected = status.HTTP_400_BAD_REQUEST
        result = response.status_code
        self.assertEqual(expected, result)
        
        
        self.assertEqual(response.data["description"][0], "This field is required.")
        self.assertEqual(response.data["price"][0], "This field is required.")
        self.assertEqual(response.data["quantity"][0], "This field is required.")
    
    def test_list_products(self):
        response = self.client.get(self.url)

        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertIn("results", response.data)
        
    def test_update_product(self):
        product_data = Product.objects.create(**self.product_1, user=self.user_seller_1)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller_1.key)
        response = self.client.patch(f'{self.url}{product_data.id}/', self.update_data)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        