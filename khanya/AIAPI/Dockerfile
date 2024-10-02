# Use a Python base image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8080

# Set the command to run the Flask app (point to api.py)
CMD ["python3", "Api.py"]
