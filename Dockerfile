FROM python:3.11

ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install — upgrade pip && pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

