# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.run:app", "--host", "0.0.0.0", "--port", "8000"]