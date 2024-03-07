import requests
import time
import unittest

delivery_url = 'http://localhost:8080'
add_food_delivery_url = f'{delivery_url}/food-delivery'
get_food_delivery_url = f'{delivery_url}/food-delivery'

delivery = {"id": 2,
            "message": "Processing food delivery for order 2",
            "delivery_id": 1}


class TestComponent(unittest.TestCase):

    def wait_for_service(self, url, max_attempts=10):
        attempts = 0
        while attempts < max_attempts:
            try:
                requests.get(url)
                break
            except requests.ConnectionError:
                time.sleep(1)
                attempts += 1

    def setUp(self):
        self.wait_for_service(delivery_url)
        # Добавьте ожидание для других микросервисов и зависимостей

    def test_create_food_delivery(self):
        res = requests.post(f"{add_food_delivery_url}/2")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Processing food delivery", res.text)

    def test_get_data_of_food_delivery(self):
        res = requests.get(f"{get_food_delivery_url}/2").json()
        self.assertEqual(res["order_id"], 2)
        self.assertEqual(res["status"], "processed")

    def test_fetch_food_delivery(self):
        res = requests.get(get_food_delivery_url)
        self.assertIn("Food Delivery not found", res.text)

    def test_cancel_food_delivery(self):
        # Отправляем DELETE-запрос для отмены доставки еды
        res = requests.delete(f"{add_food_delivery_url}/cancel/1")

        # Проверяем, что запрос завершился успешно (HTTP статус 200)
        self.assertEqual(res.status_code, 200)

        # Проверяем, что в ответе есть сообщение об отмене доставки
        self.assertTrue('message' in res.json())

if __name__ == '__main__':
    unittest.main()
