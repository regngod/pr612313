# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию /code
WORKDIR /code

# Копируем файл с зависимостями
COPY ./requirements.txt /code/
RUN pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install -r /code/requirements.txt

# Копируем код приложения
COPY ./food_delivery /code

# Копируем файл базы данных
COPY ./delivery_service/food_delivery.db /code/food_delivery.db

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "food_delivery:app", "--host", "0.0.0.0", "--port", "8000"]
