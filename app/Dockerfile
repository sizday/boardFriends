FROM python:latest
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip -r requirements.txt
COPY . /app
EXPOSE 5000
