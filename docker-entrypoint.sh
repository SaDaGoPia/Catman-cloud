#!/usr/bin/env bash
set -euo pipefail

if [[ "${AUTO_UPDATE_MAN:-1}" == "1" ]]; then
    echo "[catman] Updating man pages metadata and packages..."
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    apt-get install -y --no-install-recommends --reinstall \
        man-db \
        manpages \
        manpages-dev \
        bsdextrautils \
        coreutils \
        bash

    mandb -q || true
    rm -rf /var/lib/apt/lists/*
    echo "[catman] Man pages update completed."
else
    echo "[catman] AUTO_UPDATE_MAN=0, skipping startup man pages update."
fi

exec python app.py
