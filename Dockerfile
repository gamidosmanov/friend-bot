FROM python:3.11-slim
COPY main.py .
COPY messages.db .
RUN pip install --no-cache-dir telebot
CMD ["python", "./main.py"]