FROM python:3.11

# To show output on screen
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

# CMD python manage.py migrate
EXPOSE 8000

# replace host in settings.py if mysql connection does not work
# host.docker.internal

