FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install -r ../requirements.txt

COPY ./app /app
COPY ./models /models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
