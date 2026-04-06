# =========================
# Dockerfile
# =========================

# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install pyTelegramBotAPI

RUN chmod +x king

CMD ["python3", "bot.py"]
