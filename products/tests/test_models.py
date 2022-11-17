from django.test import TestCase
from products.models import Product
from users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_data = {
            "description": "Smartband xyz 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.user_data = {
            "username": "mat",
            "first_name": "Matheus",
            "last_name": "Freire",
            "is_seller": True
        }

    def test_model_atributes(self):
        user_data = User.objects.create_user(**self.user_data)
        product_data = Product.objects.create(**self.product_data, user=user_data)
        
        product = Product.objects.get(id=product_data.id)
        
        price_max_digits = product._meta.get_field("price").max_digits
        price_decimal = product._meta.get_field("price").decimal_places

        self.assertEqual(price_max_digits, 10)
        self.assertEqual(price_decimal, 2)