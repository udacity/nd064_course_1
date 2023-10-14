FROM python:3.8
LABEL maintainer="Thitiwat Watanajaturaporn"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# command to run on a container
CMD ["python", "app.py"]

