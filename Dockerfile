FROM python:3.8-slim

# set working dir in container
WORKDIR /app

# copy the whole file on the container
COPY . /app


RUN pip install -r requirements.txt

CMD ["python", "ali_baba.py"]