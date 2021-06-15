FROM python:3.8
LABEL maintainer='Fred'

COPY . /app
WORKDIR /app
COPY ./requirements.txt ./app/requirements.txt
RUN pip3 install -r ./app/requirements.txt
CMD ["python","app.py"] 