import unittest
import requests


class TestFoodDelivery(unittest.TestCase):
    def test_get_token(self):
        # Отправляем POST-запрос на /get-token с неправильными учетными данными
        username = "aaaaa"
        password = "123"
        response = requests.post("http://localhost:8000/get-token", data={"username": username, "password": password})

        # Проверяем, что сервер возвращает код статуса
        self.assertEqual(response.status_code, 400)

    def test_read_food_delivery(self):
        # Отправляем GET-запрос на /food-delivery/{order_id}
        order_id = 123 
        response = requests.get(f"http://localhost:8000/food-delivery/{order_id}")

        # Проверяем, что сервер возвращает код статуса
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
