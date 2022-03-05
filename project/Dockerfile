FROM python:3.8-alpine

LABEL org.opencontainers.image.source="https://github.com/bkcrouse/nd064_course_1.git"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Brian Crouse"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="Python Flask Application - TechTrends"

COPY ./techtrends/ /app/

WORKDIR /app

RUN pip install -r requirements.txt
RUN python init_db.py

EXPOSE 3111

ENTRYPOINT [ "python" ]
CMD ["app.py"]