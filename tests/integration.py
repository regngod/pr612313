import sys
import os
delivery_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../delivery_service'))
sys.path.append(delivery_service_path)

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from delivery_service import create_food_delivery_and_record, FoodDelivery, simulate_food_delivery
from sqlalchemy.exc import IntegrityError


@pytest.fixture(scope="module")
def db_session():
    # Создаем тестовую базу данных SQLite и сессию SQLAlchemy
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Создаем таблицы в тестовой базе данных
    FoodDelivery.metadata.create_all(bind=engine)

    yield session

    # Очищаем таблицы после выполнения тестов
    FoodDelivery.__table__.drop(engine)


def test_create_food_delivery_and_record(db_session):
    # Тест создания доставки еды и записи в базу данных
    order_id = 12345
    result = create_food_delivery_and_record(db_session, order_id)

    # Проверяем, что доставка создана и записана в базу данных
    assert "food_delivery_id" in result
    assert "payment_status" in result
    assert "food_status" in result

    # Проверяем, что доставка присутствует в базе данных
    db_food_delivery = db_session.query(FoodDelivery).filter(FoodDelivery.order_id == order_id).first()
    assert db_food_delivery is not None
    assert db_food_delivery.order_id == order_id
    assert db_food_delivery.status in ["delivered", "not delivered"]


def test_create_food_delivery_invalid_order_id(db_session):
    # Пытаемся создать доставку с невалидным order_id (строка вместо числа)
    invalid_order_id = "invalid_order_id"

    # Ожидаем получить TypeError, так как order_id должен быть целым числом
    with pytest.raises(TypeError):
        create_food_delivery_and_record(db_session, invalid_order_id)


if __name__ == '__main__':
    unittest.main()