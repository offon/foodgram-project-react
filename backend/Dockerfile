FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir


CMD python3 /app/foodgram/manage.py runserver

# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]