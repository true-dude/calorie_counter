FROM python:3.9-slim

WORKDIR /app

#RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

