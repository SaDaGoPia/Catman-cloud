import re
import subprocess
from flask import Flask, Response, jsonify

app = Flask(__name__)

_VALID_CMD = re.compile(r"^[a-zA-Z0-9._+-]+$")


def _man_text(command: str):
    if not _VALID_CMD.match(command):
        return None, "Comando inválido"

    proc = subprocess.run(
        ["man", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
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
        "service": "cloud-man",
        "usage": [
            "GET /man/<comando>",
            "GET /cat/<comando>"
        ]
    })


@app.get("/man/<command>")
def man_page(command: str):
    content, err = _man_text(command)
    if err:
        return jsonify({"error": err}), 404
    return Response(content, mimetype="text/plain; charset=utf-8")


@app.get("/cat/<command>")
def cat_page(command: str):
    content, err = _man_text(command)
    if err:
        return jsonify({"error": err}), 404
    return Response(content, mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
