from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from users.models import User
from products.models import Product

class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        
        cls.user_seller_data = {
            "username": "fre",
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

        
        cls.login_url = "/api/login/"
        
        
        cls.user_login_seller = {
            "username": "fre",
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
        
        cls.update_url = "/api/accounts/"
        
        cls.user_update_seller = {
            "first_name": "Freire"
        }
        
        cls.update_is_active = {
            "is_active": False
        }
        
        
    def test_register_seller(self):
        response = self.client.post(self.register_url, self.user_seller_data)
        
        expected = status.HTTP_201_CREATED
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertTrue(response.data["is_seller"])
        self.assertFalse(response.data["is_superuser"])
        
        
    def test_register_normal(self):
        response = self.client.post(self.register_url, self.user_normal_data)
        
        expected = status.HTTP_201_CREATED
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertFalse(response.data["is_seller"])
        self.assertFalse(response.data["is_superuser"])
        
    def test_register_adm(self):
        response = self.client.post(self.register_url, self.user_adm_data)
        
        expected = status.HTTP_201_CREATED
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertFalse(response.data["is_seller"])
        self.assertTrue(response.data["is_superuser"])

    def test_register_wrong_keys(self):
        response = self.client.post(self.register_url, data={})
        
        expected = status.HTTP_400_BAD_REQUEST
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertEqual(response.data["username"][0], "This field is required.")
        self.assertEqual(response.data["password"][0], "This field is required.")
        self.assertEqual(response.data["first_name"][0], "This field is required.")
        self.assertEqual(response.data["last_name"][0], "This field is required.")
        
    def test_login_seller(self):
        self.client.post(self.register_url, self.user_seller_data)
        
        response = self.client.post(self.login_url, self.user_login_seller)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertIn("token", response.data)
    
    def test_login_normal(self):
        self.client.post(self.register_url, self.user_normal_data)
        
        response = self.client.post(self.login_url, self.user_login_normal)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertIn("token", response.data)
    
    def test_login_adm(self):
        self.client.post(self.register_url, self.user_adm_data)
        
        response = self.client.post(self.login_url, self.user_login_adm)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertIn("token", response.data)
        
    
    def test_only_owner_update_fail(self):
        seller = User.objects.create_user(**self.user_seller_data)
        _ = Token.objects.create(user=seller)
        normal = User.objects.create_user(**self.user_normal_data)
        normal_token = Token.objects.create(user=normal)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + normal_token.key)
        
        response = self.client.patch(f'{self.update_url}{seller.id}/', self.user_update_seller)
        
        expected = status.HTTP_403_FORBIDDEN
        result = response.status_code
        self.assertEqual(expected, result)
    
    def test_only_owner_update(self):
        seller = User.objects.create_user(**self.user_seller_data)
        seller_token = Token.objects.create(user=seller)
        normal = User.objects.create_user(**self.user_normal_data)
        _ = Token.objects.create(user=normal)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + seller_token.key)
        
        response = self.client.patch(f'{self.update_url}{seller.id}/', self.user_update_seller)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
    
    
    def test_deactivated_account_fail(self):
        seller = User.objects.create_user(**self.user_seller_data)
        seller_token = Token.objects.create(user=seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + seller_token.key)
        
        response = self.client.patch(f'{self.update_url}{seller.id}/management/', self.update_is_active)
        
        expected = status.HTTP_403_FORBIDDEN
        result = response.status_code
        self.assertEqual(expected, result)
    
    def test_deactivated_account_fail(self):
        adm = User.objects.create_user(**self.user_adm_data)
        adm_token = Token.objects.create(user=adm)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + adm_token.key)
        
        response = self.client.patch(f'{self.update_url}{adm.id}/management/', self.update_is_active)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        self.assertEqual(response.data["is_active"], self.update_is_active["is_active"])
    
        
    def test_list(self):
        response = self.client.get(self.register_url)
        
        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(expected, result)
        
        