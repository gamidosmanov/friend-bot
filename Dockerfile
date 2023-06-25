FROM python:3.11-slim
COPY main.py .
COPY data.json .
RUN pip install telebot aiohttp pandas
CMD ["python", "./main.py"]