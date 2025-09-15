# job/Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pandas matplotlib
COPY job.py /app/job.py
ENV INPUT=/volume/csv_limpo.csv
ENV OUTPUT_DIR=/volume
CMD ["python", "/app/job.py"]
