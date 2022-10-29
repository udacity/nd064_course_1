FROM python:3.8
LABEL maintainer: Jay

COPY . /APP
WORKDIR /APP

RUN pip install -r requirements.txt

EXPOSE 311/tcp

RUN python init_db.py

CMD [ "python", "app.py" ]