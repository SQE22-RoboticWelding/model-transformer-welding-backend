FROM python:slim

# Build dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq5 \
    libpq-dev
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app /app

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
