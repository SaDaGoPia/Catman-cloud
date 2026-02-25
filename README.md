# CLOUD-MAN

Servidor HTTP en Docker que expone el contenido del manual de Linux (`man`) en texto plano.

## Endpoints

- `GET /man/<comando>`
- `GET /cat/<comando>`
- `GET /man/<seccion>/<comando>`
- `GET /health`

Ejemplo:

```bash
curl http://localhost:8080/man/ls
curl http://localhost:8080/man/5/passwd
```

---

## Ejecutar en local (sin Docker)

```bash
pip install -r requirements.txt
python app.py
```

Servidor en:

- `http://localhost:8080`

---

## Ejecutar con Docker

Construir imagen:

```bash
docker build -t cloud-man:latest .
```

Levantar contenedor:

```bash
docker run --rm -p 8080:8080 cloud-man:latest
```

Probar:

```bash
curl http://localhost:8080/man/bash
```

---

## Crear repositorio en GitHub y subir

1. Crea un repositorio vacío en GitHub (por ejemplo: `cloud-man`).
2. En esta carpeta, ejecuta:

```bash
git init
git add .
git commit -m "Initial commit: Docker Linux man server"
git branch -M main
git remote add origin https://github.com/<TU_USUARIO>/cloud-man.git
git push -u origin main
```

---

## Despliegue en la nube (opción simple con Docker)

Puedes usar cualquier servicio que acepte Dockerfile, por ejemplo:

- Render (Web Service con Docker)
- Railway (Deploy from GitHub)
- Fly.io
- Google Cloud Run

### Deploy rápido en Render

1. Entra a Render y conecta tu GitHub.
2. Selecciona el repositorio `SaDaGoPia/Catman-cloud`.
3. Render detectará `render.yaml` y creará el servicio web automáticamente.
4. Espera el primer build y abre la URL pública.
5. Prueba con:

```bash
curl https://<TU-APP-RENDER>/man/ls
```

### Parámetros mínimos

- Puerto: `8080`
- Comando de inicio: se toma de `CMD` del `Dockerfile`
- Health check recomendado: `GET /`

---

## Notas

- El servidor valida el nombre del comando para evitar inyección.
- El servidor valida también la sección de `man`.
- Se usa caché en memoria para acelerar consultas repetidas.
- Si el manual no existe, devuelve `404` con mensaje JSON.
