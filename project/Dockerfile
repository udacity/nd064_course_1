FROM python:2.7

COPY techtrends  ./

EXPOSE 3111

RUN pip install -U pip && pip install -r requirements.txt
RUN python init_db.py

ENTRYPOINT ["python", "app.py"]