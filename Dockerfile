FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
