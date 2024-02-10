# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip3 install --no-cache-dir flask

# Create the schema.sql file
RUN echo "CREATE TABLE IF NOT EXISTS points (id TEXT PRIMARY KEY, points INTEGER);" > schema.sql

# Expose the port on which the Flask app will run
EXPOSE 10001

# Command to run the Flask application
# CMD ["python3", "ReceiptProcessor.py"]

ENV FLASK_APP="ReceiptProcessor.py"

CMD [ "python3", "ReceiptProcessor.py"]
