import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import create_food_delivery_and_record, FoodDelivery

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
    assert result["order_id"] == order_id
    assert result["payment_status"] in ["paid", "pending"]
    assert result["food_status"] == "prepared"

    # Проверяем, что доставка присутствует в базе данных
    db_food_delivery = db_session.query(FoodDelivery).filter(FoodDelivery.order_id == order_id).first()
    assert db_food_delivery is not None
    assert db_food_delivery.order_id == order_id
    assert db_food_delivery.status in ["delivered", "not delivered"]

def test_create_food_delivery_duplicate(db_session):
    # Создаем доставку с определенным order_id
    order_id = 12345
    create_food_delivery_and_record(db_session, order_id)

    # Пытаемся создать доставку с тем же order_id еще раз
    # Ожидаем получить ошибку, так как заказ уже существует
    with pytest.raises(Exception):
        create_food_delivery_and_record(db_session, order_id)

    # Проверяем, что в базе данных все еще существует только одна запись с данным order_id
    count = db_session.query(FoodDelivery).filter(FoodDelivery.order_id == order_id).count()
    assert count == 1

if __name__ == '__main__':
    unittest.main()
