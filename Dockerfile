FROM python:3.7
# WORKDIR /app
# COPY ./app /app
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE $PORT
CMD ["uvicorn", "app:app", "--bind 0.0.0.0:$PORT", "--reload"]
