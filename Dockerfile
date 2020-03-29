FROM python:3.7-slim

RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*

# copy the cov19 application to /app/cov19
RUN mkdir -p /app/log

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

ADD cov19 /app/cov19
COPY web.py /app
COPY data_tracker.py /app
COPY gunicorn_start.sh /app

CMD ["./gunicorn_start.sh"]
