# version
FROM python:2.7

# Requirements
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Port
EXPOSE 6111

# command to run on container start
CMD [ "python", "init_db.py" ]
