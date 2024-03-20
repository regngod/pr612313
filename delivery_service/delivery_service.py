import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends, status, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn
import os
from keycloak.keycloak_openid import KeycloakOpenID

app = FastAPI()

KEYCLOAK_URL = "http://0.0.0.0:8180/"
KEYCLOAK_CLIENT_ID = "mandzhiev"
KEYCLOAK_REALM = "prc9"
KEYCLOAK_CLIENT_SECRET = "xYR5e9THASbiSfW9XdlsKaLxFWGbwlK1"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

user_token = ""


from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)


@app.post("/get-token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def check_user_roles():
    global user_token
    token = user_token
    try:
        # userinfo = keycloak_openid.userinfo(token["access_token"])
        token = keycloak_openid.token("regngod2", "12345")
        token_info = keycloak_openid.introspect(token["access_token"])
        if "admin1" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

# Подключение к базе данных
current_directory = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_directory, "food_delivery.db")
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей SQLAlchemy
Base = declarative_base()

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
    if (check_user_roles()):
        db = SessionLocal()
        result = create_food_delivery_and_record(db, order_id)
        db.close()
        return result
    else:
        return "Wrong JWT Token"

# GET-запрос для чтения данных о доставке еды из БД
@app.get("/food-delivery/{order_id}")
def read_food_delivery(order_id: int):
    if (check_user_roles()):
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
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)