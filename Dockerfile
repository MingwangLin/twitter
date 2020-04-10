FROM python:3.7

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV NAME Twitter


