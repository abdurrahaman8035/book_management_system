# Use the official Python base image with version specified
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY . .

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000

# Run Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
