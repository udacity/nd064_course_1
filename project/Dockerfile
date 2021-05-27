FROM python:3.8-slim-buster
LABEL maintainer="Dani"

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt && python3 init_db.py

# command to run on container start
CMD [ "python3", "app.py" ]

EXPOSE 3111/tcp
