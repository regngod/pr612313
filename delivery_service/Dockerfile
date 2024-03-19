FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./delivery_service /code

COPY ./delivery_service/food_delivery.db /code/food_delivery.db

EXPOSE 80

CMD ["python", "delivery_service.py" ]