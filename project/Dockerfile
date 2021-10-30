# Use a Python base image in version 2.7
FROM python:2.7

# Specify a maintainer
LABEL maintainer="Olena Kormachova"

# Set working directory
WORKDIR /app

# Copy files from host to container
COPY ./techtrends .

# Run pythong commands
RUN pip install -r requirements.txt
RUN python init_db.py

# Expose the application port
EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]