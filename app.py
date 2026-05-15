import time
import threading
from flask import Flask, jsonify, render_template

app = Flask(__name__)


ESTADOS = [
    {"nome": "Vermelho", "cor": "vermelho", "duracao": 30},
    {"nome": "Verde",    "cor": "verde",    "duracao": 25},
    {"nome": "Amarelo",  "cor": "amarelo",  "duracao": 4},
]

# -----------------------------------------------------------
# Estado global do semáforo (protegido por lock)
# -----------------------------------------------------------
lock = threading.Lock()
estado_atual = {
    "indice": 0,                          # índice no array ESTADOS
    "nome": ESTADOS[0]["nome"],           # nome legível
    "cor": ESTADOS[0]["cor"],             # identificador da cor
    "tempo_restante": ESTADOS[0]["duracao"],  # contador regressivo
    "duracao_total": ESTADOS[0]["duracao"],    # duração total do estado
}


def ciclo_semaforo():
    """
    Função executada em thread separada.
    Decrementa o contador a cada segundo e avança
    para o próximo estado quando o tempo se esgota.
    """
    while True:
        time.sleep(1)
        with lock:
            estado_atual["tempo_restante"] -= 1

            # Quando o tempo acaba, avança para o próximo estado
            if estado_atual["tempo_restante"] <= 0:
                estado_atual["indice"] = (estado_atual["indice"] + 1) % len(ESTADOS)
                proximo = ESTADOS[estado_atual["indice"]]
                estado_atual["nome"] = proximo["nome"]
                estado_atual["cor"] = proximo["cor"]
                estado_atual["tempo_restante"] = proximo["duracao"]
                estado_atual["duracao_total"] = proximo["duracao"]


# -----------------------------------------------------------
# Inicia a thread do ciclo (daemon para encerrar com o app)
# -----------------------------------------------------------
thread = threading.Thread(target=ciclo_semaforo, daemon=True)
thread.start()


# ========================= ROTAS ===========================

@app.route("/")
def index():
    """Serve a página principal do simulador."""
    return render_template("index.html")


@app.route("/status")
def status():
    """Retorna o estado atual do semáforo em JSON."""
    with lock:
        return jsonify({
            "nome": estado_atual["nome"],
            "cor": estado_atual["cor"],
            "tempo_restante": estado_atual["tempo_restante"],
            "duracao_total": estado_atual["duracao_total"],
        })


@app.route("/reset", methods=["POST"])
def reset():
    """Reinicia o ciclo do semáforo para o estado Vermelho."""
    with lock:
        estado_atual["indice"] = 0
        primeiro = ESTADOS[0]
        estado_atual["nome"] = primeiro["nome"]
        estado_atual["cor"] = primeiro["cor"]
        estado_atual["tempo_restante"] = primeiro["duracao"]
        estado_atual["duracao_total"] = primeiro["duracao"]
    return jsonify({"mensagem": "Ciclo reiniciado com sucesso."})


# -----------------------------------------------------------
# Execução principal
# -----------------------------------------------------------
if __name__ == "__main__":
    print("[SEMAFORO] Simulador rodando em http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
