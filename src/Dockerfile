FROM python:slim

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app /app

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
