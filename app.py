import re
import subprocess
from functools import lru_cache
from flask import Flask, Response, jsonify

app = Flask(__name__)

_VALID_CMD = re.compile(r"^[a-zA-Z0-9._+-]+$")
_VALID_SECTION = re.compile(r"^[0-9a-zA-Z]+$")


@lru_cache(maxsize=256)
def _man_text(command: str, section: str | None = None):
    if not _VALID_CMD.match(command):
        return None, "Comando inválido"
    if section is not None and not _VALID_SECTION.match(section):
        return None, "Sección inválida"

    man_args = ["man"]
    if section is not None:
        man_args.append(section)
    man_args.append(command)

    proc = subprocess.run(
        man_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=8
    )

    if proc.returncode != 0:
        return None, proc.stderr.strip() or f"No se encontró manual para: {command}"

    clean = subprocess.run(
        ["col", "-b"],
        input=proc.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if clean.returncode != 0:
        return None, clean.stderr.strip() or "Error limpiando formato del manual"

    return clean.stdout, None


@app.get("/")
def home():
    return jsonify({
        "service": "catman-cloud",
        "status": "ok",
        "usage": [
            "GET /man/<comando>",
            "GET /cat/<comando>",
            "GET /man/<seccion>/<comando>",
            "GET /health"
        ],
        "examples": [
            "/man/ls",
            "/man/5/passwd",
            "/cat/bash"
        ]
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/man/<command>")
def man_page(command: str):
    content, err = _man_text(command)
    if err:
        status = 400 if err in {"Comando inválido", "Sección inválida"} else 404
        return jsonify({"error": err}), status
    return Response(content, mimetype="text/plain; charset=utf-8")


@app.get("/man/<section>/<command>")
def man_page_section(section: str, command: str):
    content, err = _man_text(command, section)
    if err:
        status = 400 if err in {"Comando inválido", "Sección inválida"} else 404
        return jsonify({"error": err}), status
    return Response(content, mimetype="text/plain; charset=utf-8")


@app.get("/cat/<command>")
def cat_page(command: str):
    content, err = _man_text(command)
    if err:
        status = 400 if err in {"Comando inválido", "Sección inválida"} else 404
        return jsonify({"error": err}), status
    return Response(content, mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
