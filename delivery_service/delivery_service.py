import sqlalchemy
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Подключение к базе данных
DATABASE_URL = "sqlite:///./food_delivery.db"  # Изменил имя базы данных
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей SQLAlchemy
Base = sqlalchemy.orm.declarative_base()

# Определение модели FoodDelivery
class FoodDelivery(Base):
    __tablename__ = "food_deliveries"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    status = Column(String)

# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создание сессии SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Моковая функция для имитации обработки оплаты и подготовки блюда
def simulate_food_delivery(order_id: int):
    payment_status = "paid" if order_id % 2 == 0 else "pending"
    return {"order_id": order_id, "payment_status": payment_status, "food_status": "prepared"}

# Функция для создания доставки еды и записи в БД
def create_food_delivery_and_record(db, order_id: int):
    food_delivery_result = simulate_food_delivery(order_id)
    delivery_status = "delivered" if food_delivery_result["payment_status"] == "paid" else "not delivered"

    # Создание объекта FoodDelivery и добавление в БД
    db_food_delivery = FoodDelivery(order_id=order_id, status=delivery_status)
    db.add(db_food_delivery)
    db.commit()
    db.refresh(db_food_delivery)

    return {
        "message": f"Food delivery for order {order_id} {delivery_status}",
        "food_delivery_id": db_food_delivery.id,
        "payment_status": food_delivery_result["payment_status"],
        "food_status": food_delivery_result["food_status"],
    }

# POST-запрос для создания доставки еды
@app.post("/food-delivery/{order_id}")
def create_food_delivery(order_id: int):
    db = SessionLocal()
    result = create_food_delivery_and_record(db, order_id)
    db.close()
    return result

# GET-запрос для чтения данных о доставке еды из БД
@app.get("/food-delivery/{order_id}")
def read_food_delivery(order_id: int):
    db = SessionLocal()
    food_delivery = db.query(FoodDelivery).filter(FoodDelivery.order_id == order_id).first()
    db.close()

    if not food_delivery:
        raise HTTPException(status_code=404, detail="Food delivery not found")

    return {
        "order_id": food_delivery.order_id,
        "status": food_delivery.status,
        "payment_status": "paid" if food_delivery.status == "delivered" else "pending",
        "food_status": "prepared",
    }
