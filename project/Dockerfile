FROM python:3.8
LABEL maintainer="Przemyslaw Sulecki"

WORKDIR /app
COPY ./project/techtrends/ /app

RUN pip install -r requirements.txt
RUN python init_db.py

ENV FLASK_APP=app

EXPOSE 3111

CMD [ "python", "app.py" ]