# etl/Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pandas
COPY etl.py /app/etl.py
# INPUT e OUTPUT_DIR são configuráveis; por padrão usamos /volume
ENV INPUT=/volume/ingest.csv
ENV OUTPUT_DIR=/volume
CMD ["python", "/app/etl.py"]
