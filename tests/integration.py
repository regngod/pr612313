import sys
import os
from unittest.mock import MagicMock

delivery_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../delivery_service'))
sys.path.append(delivery_service_path)

import pytest
from delivery_service import create_food_delivery_and_record, simulate_food_delivery

@pytest.fixture(scope="module")
def db_session():
    # Создаем фиктивный объект базы данных
    return MagicMock()

def test_create_food_delivery_and_record(db_session):
    # Тест создания доставки еды и записи в базу данных
    order_id = 12345
    result = create_food_delivery_and_record(db_session, order_id)

    # Проверяем, что доставка создана и записана в базу данных
    assert "food_delivery_id" in result
    assert "payment_status" in result
    assert "food_status" in result

    # Проверяем, что была вызвана функция add хотя бы один раз
    db_session.add.assert_called_once()

def test_create_food_delivery_invalid_order_id(db_session):
    # Пытаемся создать доставку с невалидным order_id (строка вместо числа)
    invalid_order_id = "invalid_order_id"

    # Ожидаем получить TypeError, так как order_id должен быть целым числом
    with pytest.raises(TypeError):
        create_food_delivery_and_record(db_session, invalid_order_id)


if __name__ == '__main__':
    unittest.main()

