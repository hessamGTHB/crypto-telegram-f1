FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# .env را در کنار docker-compose یا با docker run -e پاس دهید
CMD ["python", "bot.py"]
