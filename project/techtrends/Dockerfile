FROM python:2.7
EXPOSE 3111
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
RUN python init_db.py
CMD [ "python", "app.py"]
