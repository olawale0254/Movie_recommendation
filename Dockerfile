FROM python:3.7
# WORKDIR /app
# COPY ./app /app
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--reload"]
