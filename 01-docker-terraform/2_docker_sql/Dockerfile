FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg

WORKDIR /app
COPY ingest_data_hw.py ingest_data_hw.py

ENTRYPOINT [ "python", "ingest_data_hw.py"]
