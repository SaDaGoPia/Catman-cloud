FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

RUN apt-get update \
    && find /etc/dpkg/dpkg.cfg.d -type f -print0 | xargs -0 -r sed -i '/\/usr\/share\/man\//d' \
    && apt-get install -y --no-install-recommends --reinstall man-db manpages manpages-dev bsdextrautils coreutils bash \
    && mandb -q \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY docker-entrypoint.sh .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]
