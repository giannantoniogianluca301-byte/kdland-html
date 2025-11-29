from flask import Flask, request, jsonify, send_file
import random
import json
import os

app = Flask(__name__)

CLASSIFICA_FILE = "classifica.json"

def leggi_classifica():
    if not os.path.exists(CLASSIFICA_FILE):
        return {}
    with open(CLASSIFICA_FILE, "r") as f:
        return json.load(f)

def salva_classifica(classifica):
    with open(CLASSIFICA_FILE, "w") as f:
        json.dump(classifica, f)

@app.route('/')
def home():
    return send_file("index.html")

@app.route('/gioca', methods=["POST"])
def gioca():
    nome = request.form.get("nome", "").strip()
    scelta = request.form.get("scelta", "")
    try:
        puntata = int(request.form.get("puntata", "0"))
    except ValueError:
        return jsonify({"errore": "Inserisci un numero valido per la puntata!"})

    if not nome:
        return jsonify({"errore": "Inserisci il tuo nome!"})
    if scelta not in ["Testa", "Croce"]:
        return jsonify({"errore": "Scegli Testa o Croce!"})
    if puntata <= 0:
        return jsonify({"errore": "La puntata deve essere maggiore di 0."})

    classifica = leggi_classifica()
    saldo = classifica.get(nome, 100)

    if puntata > saldo:
        return jsonify({"errore": "Non hai abbastanza soldi per questa puntata."})

    risultato = random.choice(["Testa", "Croce"])

    if risultato == scelta:
        saldo += puntata
        esito = f"vinto {puntata}$"
    else:
        saldo -= puntata
        esito = f"perso {puntata}$"

    classifica[nome] = saldo
    salva_classifica(classifica)

    return jsonify({"esito": esito, "risultato": risultato, "saldo": saldo})

@app.route('/classifica')
def classifica():
    classifica = leggi_classifica()
    sorted_classifica = sorted(classifica.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_classifica)

if __name__ == '__main__':
    app.run(debug=True)
