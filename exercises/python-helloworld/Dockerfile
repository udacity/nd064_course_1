FROM python:2.7.18-slim
LABEL maintainer=thiagomsdev@gmail.com

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]

