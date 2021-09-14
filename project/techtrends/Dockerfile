# version
FROM python:2.7
LABEL maintainer="Andrea Gutierrez"
RUN python -m pip install --upgrade pip

# Requirements
ADD . /app
#COPY techtrends/requirements.txt /app/requirements.txt
#COPY techtrends/init_db.py /app/init_db.py
WORKDIR /app

#install requirements.txt file and db in init_db.py
RUN pip install -r requirements.txt
RUN python /app/init_db.py

# Port
EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]