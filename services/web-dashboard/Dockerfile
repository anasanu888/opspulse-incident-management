FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY common ./common
COPY services/web-dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/web-dashboard/app.py .
EXPOSE 5000
CMD ["python","app.py"]
