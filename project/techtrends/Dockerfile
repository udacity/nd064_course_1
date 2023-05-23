# Use a Python base image in version 3.8
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Expose the application port 3111
EXPOSE 3111

# Install packages defined in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Ensure that the database is initialized with the pre-defined posts in the init_db.py file
RUN python init_db.py

# Set the entry point to run the application
CMD [ "python", "app.py" ]
