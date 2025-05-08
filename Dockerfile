FROM python:3.11-slim

WORKDIR /app

# Установка wait-for-it
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["wait-for-it.sh", "db:5432", "--", "python", "backend/manage.py", "runserver", "0.0.0.0:8000"]