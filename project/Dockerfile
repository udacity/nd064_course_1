FROM python:2.7

WORKDIR /home/app

COPY techtrends /home/app/

RUN pip install --no-cache-dir -r requirements.txt

RUN python init_db.py

EXPOSE 3111

ENTRYPOINT ["python","app.py"]
