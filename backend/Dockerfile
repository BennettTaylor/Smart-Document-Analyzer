# Use the official Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the backend files into the container
COPY . /app

# Install any Python dependencies (if needed)
RUN pip install -r requirements.txt

# Expose the port your application runs on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "app.py"]