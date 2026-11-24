FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY common ./common
COPY services/event-ingestor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/event-ingestor/worker.py .
CMD ["python","worker.py"]
