# version
FROM python:2.7
LABEL maintainer="Andrea Gutierrez"

#Before running everything
RUN python -m pip install --upgrade pip

# Requirements
COPY ./techtrends /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python init_db.py

# Port
EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py"]