FROM python:3.8

WORKDIR /app

COPY ./techtrends/requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./techtrends /app

EXPOSE 3111

RUN python init_db.py

CMD ["python", "app.py"]