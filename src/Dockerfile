FROM python:slim

# Build dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq5 \
    libpq-dev
RUN pip install --upgrade pip

COPY . /
RUN pip install -r /requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
