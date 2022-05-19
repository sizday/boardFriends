FROM python:latest
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip -r requirements.txt
COPY .. /app
RUN pip install -r requirements.txt
