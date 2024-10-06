# Use an official Django runtime as a parent image
FROM python:3.11-alpine
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev g++ expect

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN rm db.sqlite3 || true
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN /app/tests/create_admin.exp
RUN python manage.py auto_create

# Set the environment variable for Python
ENV PYTHONUNBUFFERED=1

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django migrations and start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
