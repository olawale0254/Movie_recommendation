FROM python:3.8

WORKDIR /app
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--reload"]

COPY src/* /app/
COPY data/* /app/
RUN pip install -r requirements.txt
