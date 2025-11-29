from flask import Flask, request, render_template, redirect
import uuid
import random
import socket

# ============================================
# Obtener IP local para mostrarla al arrancar
# ============================================
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No hace falta que 8.8.8.8 esté accesible. Ni se envían datos.
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

print("========================================")
print("🟢 Servidor listo en:")
print(f"➡️  http://{get_local_ip()}:8501")
print("========================================")


# ============================================
# APP FLASK
# ============================================
app = Flask(__name__)

participants = {}      # session_id → name
assignments = {}       # name → receiver
sort_done = False


# ============================================
# Rutas principales
# ============================================

@app.route("/")
def index():
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())

    user_name = participants.get(session_id)
    receiver = assignments.get(user_name)

    # Detectar si es host (quien ejecuta el servidor)
    client_ip = request.remote_addr
    server_ip = request.host.split(":")[0]
    is_host = client_ip == server_ip or client_ip == "127.0.0.1"

    resp = app.make_response(render_template(
        "index.html",
        participants=list(participants.values()),
        user_name=user_name,
        receiver=receiver,
        sort_done=sort_done,
        session_id=session_id,
        is_host=is_host
    ))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name").strip()
    session_id = request.cookies.get("session_id") or str(uuid.uuid4())

    if name:
        participants[session_id] = name

    resp = redirect("/", code=303)
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sort", methods=["POST"])
def sort():
    global sort_done
    names = list(participants.values())

    if len(names) >= 2:
        shuffled = names[:]
        while True:
            random.shuffle(shuffled)
            if all(shuffled[i] != names[i] for i in range(len(names))):
                break

        for a, b in zip(names, shuffled):
            assignments[a] = b

        sort_done = True

    return redirect("/", code=303)


# ============================================
# Lanzar servidor
# ============================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=False)