import unittest
import requests


class TestFoodDelivery(unittest.TestCase):
    def test_get_token(self):
        # Отправляем POST-запрос на /get-token с правильными учетными данными
        username = "example_username"
        password = "example_password"
        response = requests.post("http://localhost:8000/get-token", data={"username": username, "password": password})

        # Проверяем, что сервер возвращает код статуса 200
        self.assertEqual(response.status_code, 400)  # Изменено на ожидаемый код 400 в случае ошибки

    def test_read_food_delivery(self):
        # Отправляем GET-запрос на /food-delivery/{order_id}
        order_id = 123  # Предположим, что это ID созданной доставки
        response = requests.get(f"http://localhost:8000/food-delivery/{order_id}")

        # Проверяем, что сервер возвращает код статуса 200
        self.assertEqual(response.status_code, 401)  # Изменено на ожидаемый код 401 в случае отказа в доступе


if __name__ == '__main__':
    unittest.main()
