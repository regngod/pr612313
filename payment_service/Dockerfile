FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./payment_service /code

COPY ./payment_service/payment.db /code/payment.db

EXPOSE 8000

CMD ["uvicorn", "payment_service:app", "--host", "127.0.0.1", "--port", "80" ]