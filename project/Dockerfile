FROM python:2.7
EXPOSE 3111
COPY ./techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python init_db.py
CMD [ "python", "app.py"]
