# CLOUD-MAN

HTTP server running in Docker that exposes Linux manual (`man`) content as plain text.

## Endpoints

- `GET /man/<command>`
- `GET /cat/<command>`
- `GET /man/<section>/<command>`
- `GET /health`

Example:

```bash
curl http://localhost:8080/man/ls
curl http://localhost:8080/man/5/passwd
```

---

## Run locally (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

Server URL:

- `http://localhost:8080`

---

## Run with Docker

Build image:

```bash
docker build -t cloud-man:latest .
```

Run container:

```bash
docker run --rm -p 8080:8080 cloud-man:latest
```

Test:

```bash
curl http://localhost:8080/man/bash
```

---

## Create and push GitHub repository

1. Create an empty repository on GitHub (for example: `cloud-man`).
2. In this folder, run:

```bash
git init
git add .
git commit -m "Initial commit: Docker Linux man server"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/cloud-man.git
git push -u origin main
```

---

## Cloud deployment (simple Docker option)

You can use any service that accepts a Dockerfile, for example:

- Render (Web Service with Docker)
- Railway (Deploy from GitHub)
- Fly.io
- Google Cloud Run

### Quick deploy on Render

1. Go to Render and connect your GitHub account.
2. Select repository `SaDaGoPia/Catman-cloud`.
3. Render will detect `render.yaml` and create the web service automatically.
4. Wait for the first build and open the public URL.
5. Test with:

```bash
curl https://<YOUR-RENDER-APP>/man/ls
```

### Minimum parameters

- Port: `8080`
- Startup command: taken from `CMD` in `Dockerfile`
- Recommended health check: `GET /`

---

## Notes

- The server validates command names to prevent injection.
- The server also validates the `man` section.
- In-memory caching is used to speed up repeated lookups.
- If a manual page is not found, it returns `404` with a JSON message.
