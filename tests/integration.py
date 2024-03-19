import unittest
import os
import sys
import requests
import time

# Добавляем путь к модулю delivery_service для корректного импорта
delivery_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../delivery_service'))
sys.path.append(delivery_service_path)

# Импортируем необходимые компоненты для тестирования
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from delivery_service import create_food_delivery_and_record, FoodDelivery

class TestComponent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем тестовую базу данных SQLite и сессию SQLAlchemy
        cls.engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        cls.session = SessionLocal()

        # Создаем таблицы в тестовой базе данных
        FoodDelivery.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Очищаем таблицы после выполнения всех тестов
        FoodDelivery.__table__.drop(cls.engine)

    def wait_for_service(self, url, max_attempts=10):
        # Ожидаем доступности сервиса по указанному URL-адресу
        attempts = 0
        while attempts < max_attempts:
            try:
                requests.get(url)
                break
            except requests.ConnectionError:
                time.sleep(1)
                attempts += 1

    def setUp(self):
        # Ожидаем доступности сервиса перед каждым тестом
        self.wait_for_service('http://localhost:8000')

    def test_create_food_delivery(self):
        # Тест создания доставки еды и проверки HTTP-статуса
        res = requests.post('http://localhost:8000/food-delivery/2')
        self.assertEqual(res.status_code, 200)

    def test_get_data_of_food_delivery(self):
        # Тест получения данных о доставке еды и проверки содержимого
        res = requests.get('http://localhost:8000/food-delivery/2').json()
        self.assertIn("order_id", res)
        self.assertIn("status", res)
        self.assertEqual(res["order_id"], 2)

    def test_fetch_food_delivery(self):
        # Тест на запрос данных о несуществующей доставке еды и проверку HTTP-статуса
        res = requests.get('http://localhost:8000/food-delivery/100')
        self.assertEqual(res.status_code, 404)

    def test_cancel_food_delivery(self):
        # Тест на отмену доставки еды и проверку HTTP-статуса
        res = requests.delete('http://localhost:8000/food-delivery/cancel/1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('message' in res.json())

if __name__ == '__main__':
    unittest.main()
