FROM python:3.8
LABEL maintainer="Guy Bourne"

EXPOSE 3111
COPY techtrends /techtrends
WORKDIR /techtrends
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python init_db.py

# command to run on container start
CMD [ "python", "app.py" ]
