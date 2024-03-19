import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from delivery_service import create_food_delivery_and_record, FoodDelivery, simulate_food_delivery
from sqlalchemy.exc import IntegrityError

class TestFoodDelivery(unittest.TestCase):
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

    def test_create_food_delivery_and_record(self):
        # Тест создания доставки еды и записи в базу данных
        order_id = 12345
        result = create_food_delivery_and_record(self.session, order_id)

        # Проверяем, что доставка создана и записана в базу данных
        self.assertIn("food_delivery_id", result)
        self.assertIn("payment_status", result)
        self.assertIn("food_status", result)

        # Проверяем, что доставка присутствует в базе данных
        db_food_delivery = self.session.query(FoodDelivery).filter(FoodDelivery.order_id == order_id).first()
        self.assertIsNotNone(db_food_delivery)
        self.assertEqual(db_food_delivery.order_id, order_id)
        self.assertIn(db_food_delivery.status, ["delivered", "not delivered"])

    def test_create_food_delivery_invalid_order_id(self):
        # Пытаемся создать доставку с невалидным order_id (строка вместо числа)
        invalid_order_id = "invalid_order_id"

        # Ожидаем получить TypeError, так как order_id должен быть целым числом
        with self.assertRaises(TypeError):
            create_food_delivery_and_record(self.session, invalid_order_id)

if __name__ == '__main__':
    unittest.main()
