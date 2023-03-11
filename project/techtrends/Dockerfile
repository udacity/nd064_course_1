FROM python:3.8-slim-bullseye

LABEL maintainer="Gabriel Enriquez"

#install dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip install --requirement requirements.txt

#copy app
COPY . .

#init DB. Ideally, we want to have 1 DB for a cluster, vs each pod having its own DB.
# anyways, just for test/fun/learning experience
RUN python init_db.py

EXPOSE 3111
# command to run on container start
CMD [ "python", "app.py" ]