FROM continuumio/anaconda3:latest
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN conda update conda
# Add community repository, since e.g. FastAPI is not available in the official repos
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict

COPY requirements.txt /app/
RUN conda create --name sqe-backend --file /app/requirements.txt
COPY ./app /app

CMD ["conda", "run", "-n", "sqe-backend", "uvicorn", "--host", "0.0.0.0", "app.main:app"]
