FROM python:3.8-slim

# set working dir in container
WORKDIR /app

# copy requirements.txt on app first
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# copy the whole file on the container
COPY . /app

CMD ["python", "ali_baba.py"]