# Catman Cloud

Catman Cloud is a Dockerized HTTP API that serves Linux manual pages from `man`.
It supports plain-text output for command docs and JSON responses for service metadata and errors.

## API

- `GET /` service info and usage (JSON)
- `GET /health` health check (JSON)
- `GET /man/<command>` manual page by command (plain text)
- `GET /man/<section>/<command>` manual page by section and command (plain text)
- `GET /cat/<command>` alias of `/man/<command>` (plain text)

Examples:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/man/ls
curl http://localhost:8080/man/5/passwd
```

## How it stays up to date

The container is configured to refresh man-related packages on every startup:

- runs `apt-get update`
- reinstalls `man-db`, `manpages`, `manpages-dev`, `coreutils`, `bash`, and `bsdextrautils`
- rebuilds the man index with `mandb`

This solves the common `python:slim` issue where many command manpages (like `ls`) are missing.

### Startup behavior control

By default, updates are enabled.

Disable startup refresh with:

```bash
docker run --rm -e AUTO_UPDATE_MAN=0 -p 8080:8080 catman-cloud:latest
```

## Local run (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

Service URL: `http://localhost:8080`

## Docker run

Build:

```bash
docker build -t catman-cloud:latest .
```

Run:

```bash
docker run --rm -p 8080:8080 catman-cloud:latest
```

## Cloud deploy

The repository includes `render.yaml` for quick Render deployment.

### Render quick deploy

1. Connect GitHub in Render.
2. Select repository `SaDaGoPia/Catman-cloud`.
3. Deploy as Blueprint (`render.yaml` is auto-detected).
4. Test after deployment:

```bash
curl https://<YOUR-RENDER-APP>/health
curl https://<YOUR-RENDER-APP>/man/ls
```

## Notes

- Input is validated to reduce command/section injection risk.
- Manual-page responses are plain text.
- Service metadata and error responses are JSON.
- Startup updates require network access and increase container startup time.
