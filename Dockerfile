# Use a Python base image in version 3.8
FROM python:3.8-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the TechTrends application files to the container
COPY ./techtrends /app

# Expose the application port 3111
EXPOSE 3111

# Install packages defined in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Ensure that the database is initialized with the pre-defined posts
RUN python init_db.py

# Set the command to execute the application at container start
CMD ["python", "app.py"]