FROM python:3.7-slim

RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*

# copy the cov19 application to /opt/cov19
RUN mkdir -p /app/log

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY cov19/cov19.py .

# Copy hello-cron file to the cron.d directory
COPY cov19/cov19-cron /etc/cron.d/cov19-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cov19-cron

# Apply cron job
RUN crontab /etc/cron.d/cov19-cron

# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log

CMD ["cron", "-f"]
# CMD ["/bin/sh"]