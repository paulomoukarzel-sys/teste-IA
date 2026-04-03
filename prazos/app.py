"""
Controle de Prazos e Compromissos — Gastão da Rosa & Moukarzel
Flask + SQLite, porta 5001
"""
import os, json, sqlite3, threading, time
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "prazos.db")

# ─── Banco de dados ────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS prazos (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                data_prazo      TEXT,
                cliente         TEXT NOT NULL,
                compromisso     TEXT NOT NULL,
                tipo            TEXT NOT NULL DEFAULT 'prazo',
                tribunal        TEXT,
                partes          TEXT,
                resumo          TEXT,
                status          TEXT NOT NULL DEFAULT 'pendente',
                alerta_dia_ant  INTEGER DEFAULT 0,
                alerta_no_dia   INTEGER DEFAULT 0,
                criado_em       TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        # Migração: adiciona colunas novas se não existirem (banco já criado)
        for col, defn in [("tribunal","TEXT"), ("partes","TEXT"),
                          ("data_prazo_nullable","TEXT")]:
            try:
                if col == "data_prazo_nullable":
                    pass  # tratado na lógica, não precisa de coluna extra
                else:
                    db.execute(f"ALTER TABLE prazos ADD COLUMN {col} {defn}")
            except Exception:
                pass
        db.commit()

# ─── Helpers ──────────────────────────────────────────────────────────────────

def row_to_dict(row):
    d = dict(row)
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    dp = d.get("data_prazo") or ""
    if d["status"] == "pendente":
        if not dp:
            d["urgencia"] = "sem_data"
        elif dp < today:
            d["urgencia"] = "vencido"
        elif dp == today:
            d["urgencia"] = "hoje"
        elif dp == tomorrow:
            d["urgencia"] = "amanha"
        else:
            d["urgencia"] = "normal"
    else:
        d["urgencia"] = d["status"]
    return d

# ─── Rotas ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/prazos", methods=["GET"])
def listar():
    status_f = request.args.get("status", "")
    tipo_f   = request.args.get("tipo", "")
    with get_db() as db:
        q = "SELECT * FROM prazos WHERE 1=1"
        params = []
        if status_f:
            q += " AND status=?"
            params.append(status_f)
        if tipo_f:
            q += " AND tipo=?"
            params.append(tipo_f)
        q += " ORDER BY data_prazo ASC, id ASC"
        rows = db.execute(q, params).fetchall()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/prazos", methods=["POST"])
def criar():
    d = request.json
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO prazos (data_prazo,cliente,compromisso,tipo,tribunal,partes,resumo) VALUES (?,?,?,?,?,?,?)",
            (d.get("data_prazo") or None, d["cliente"], d["compromisso"],
             d.get("tipo","prazo"), d.get("tribunal",""), d.get("partes",""),
             d.get("resumo",""))
        )
        db.commit()
        row = db.execute("SELECT * FROM prazos WHERE id=?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201

@app.route("/api/prazos/<int:pid>", methods=["PUT"])
def atualizar(pid):
    d = request.json
    fields, params = [], []
    for k in ("data_prazo","cliente","compromisso","tipo","tribunal","partes","resumo","status"):
        if k in d:
            fields.append(f"{k}=?")
            params.append(d[k])
    params.append(pid)
    with get_db() as db:
        db.execute(f"UPDATE prazos SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
        row = db.execute("SELECT * FROM prazos WHERE id=?", (pid,)).fetchone()
    return jsonify(row_to_dict(row))

@app.route("/api/prazos/<int:pid>", methods=["DELETE"])
def deletar(pid):
    with get_db() as db:
        db.execute("DELETE FROM prazos WHERE id=?", (pid,))
        db.commit()
    return jsonify({"ok": True})

@app.route("/api/stats")
def stats():
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    with get_db() as db:
        total     = db.execute("SELECT COUNT(*) FROM prazos WHERE status='pendente'").fetchone()[0]
        hoje      = db.execute("SELECT COUNT(*) FROM prazos WHERE status='pendente' AND data_prazo=?", (today,)).fetchone()[0]
        amanha    = db.execute("SELECT COUNT(*) FROM prazos WHERE status='pendente' AND data_prazo=?", (tomorrow,)).fetchone()[0]
        vencidos  = db.execute("SELECT COUNT(*) FROM prazos WHERE status='pendente' AND data_prazo<?", (today,)).fetchone()[0]
        concluidos= db.execute("SELECT COUNT(*) FROM prazos WHERE status='concluido'").fetchone()[0]
    return jsonify({"total":total,"hoje":hoje,"amanha":amanha,"vencidos":vencidos,"concluidos":concluidos})

# ─── SSE: push de alertas ─────────────────────────────────────────────────────

alert_queue = []
alert_lock  = threading.Lock()

def _check_alerts():
    """Verifica alertas a cada 60 s e empurra para a fila SSE."""
    while True:
        time.sleep(60)
        today    = date.today().isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        with get_db() as db:
            # alertas para amanhã (ainda não enviados)
            rows = db.execute(
                "SELECT * FROM prazos WHERE status='pendente' AND data_prazo=? AND alerta_dia_ant=0",
                (tomorrow,)
            ).fetchall()
            for r in rows:
                msg = {"tipo":"amanha","id":r["id"],"cliente":r["cliente"],
                       "compromisso":r["compromisso"],"data":r["data_prazo"]}
                with alert_lock:
                    alert_queue.append(msg)
                db.execute("UPDATE prazos SET alerta_dia_ant=1 WHERE id=?", (r["id"],))
            # alertas para hoje
            rows = db.execute(
                "SELECT * FROM prazos WHERE status='pendente' AND data_prazo=? AND alerta_no_dia=0",
                (today,)
            ).fetchall()
            for r in rows:
                msg = {"tipo":"hoje","id":r["id"],"cliente":r["cliente"],
                       "compromisso":r["compromisso"],"data":r["data_prazo"]}
                with alert_lock:
                    alert_queue.append(msg)
                db.execute("UPDATE prazos SET alerta_no_dia=1 WHERE id=?", (r["id"],))
            db.commit()

@app.route("/api/alertas/stream")
def alertas_stream():
    def gen():
        yield "data: {\"ping\":true}\n\n"
        while True:
            with alert_lock:
                if alert_queue:
                    msg = alert_queue.pop(0)
                    yield f"data: {json.dumps(msg, ensure_ascii=False)}\n\n"
            time.sleep(2)
    return Response(gen(), mimetype="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

@app.route("/api/alertas/pendentes")
def alertas_pendentes():
    """Retorna alertas que deveriam ter sido emitidos (para exibir ao abrir o app)."""
    today    = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    with get_db() as db:
        rows_hj  = db.execute("SELECT * FROM prazos WHERE status='pendente' AND data_prazo=?", (today,)).fetchall()
        rows_amh = db.execute("SELECT * FROM prazos WHERE status='pendente' AND data_prazo=?", (tomorrow,)).fetchall()
    alerts = []
    for r in rows_hj:
        alerts.append({"tipo":"hoje","id":r["id"],"cliente":r["cliente"],
                        "compromisso":r["compromisso"],"data":r["data_prazo"]})
    for r in rows_amh:
        alerts.append({"tipo":"amanha","id":r["id"],"cliente":r["cliente"],
                        "compromisso":r["compromisso"],"data":r["data_prazo"]})
    return jsonify(alerts)

# ─── Sincronização de E-mail ──────────────────────────────────────────────────

EMAIL_CONFIG = os.path.join(os.path.dirname(__file__), "email_config.json")
_sync_status = {"rodando": False, "ultimo": None, "resultado": None}

@app.route("/api/email/status")
def email_status():
    cfg_existe = os.path.exists(EMAIL_CONFIG)
    return jsonify({**_sync_status, "configurado": cfg_existe})

@app.route("/api/email/sync", methods=["POST"])
def email_sync():
    if _sync_status["rodando"]:
        return jsonify({"ok": False, "msg": "Sincronização já em andamento."}), 409
    if not os.path.exists(EMAIL_CONFIG):
        return jsonify({"ok": False, "msg": "E-mail não configurado. Execute configurar_email.py."}), 400

    def _run():
        _sync_status["rodando"] = True
        try:
            # Usa Graph API (Hotmail/Outlook pessoal) se token existir
            graph_token = os.path.join(os.path.dirname(__file__), "graph_token.json")
            if os.path.exists(graph_token):
                from leitor_email_graph import sincronizar_graph
                res = sincronizar_graph()
            else:
                from leitor_email import sincronizar, carregar_config
                cfg = carregar_config()
                res = sincronizar(cfg)
            _sync_status["resultado"] = res
            _sync_status["ultimo"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            _sync_status["resultado"] = {"msg": str(e), "novos": 0, "erros": 1}
        finally:
            _sync_status["rodando"] = False

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return jsonify({"ok": True, "msg": "Sincronização iniciada."})

def _daemon_email():
    """Loop de sync automático quando email_config.json existir."""
    import time as _time
    while True:
        _time.sleep(60)  # verifica a cada minuto se é hora de sincronizar
        if not os.path.exists(EMAIL_CONFIG):
            continue
        try:
            with open(EMAIL_CONFIG, encoding="utf-8") as f:
                cfg = json.load(f)
            intervalo = cfg.get("intervalo_minutos", 30) * 60
            ultimo = _sync_status.get("_ts_ultimo", 0)
            import time as _t
            if _t.time() - ultimo >= intervalo and not _sync_status["rodando"]:
                _sync_status["_ts_ultimo"] = _t.time()
                from leitor_email import sincronizar
                _sync_status["rodando"] = True
                try:
                    res = sincronizar(cfg)
                    _sync_status["resultado"] = res
                    _sync_status["ultimo"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                except Exception as e:
                    _sync_status["resultado"] = {"msg": str(e), "novos": 0, "erros": 1}
                finally:
                    _sync_status["rodando"] = False
        except Exception:
            pass

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    threading.Thread(target=_check_alerts, daemon=True).start()
    threading.Thread(target=_daemon_email,  daemon=True).start()
    print("Controle de Prazos rodando em http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=False)
