import threading
import time
import socket
import json
import os
from collections import defaultdict
import heapq
import sys

# === CONFIG ===
ID = os.getenv("ID") or sys.argv[1].lower()  # ou use como argumento: python router.py R1
PORTA_BASE = 5000

vizinhanca = {}  # ex: { "R2": 4, "R3": 2 }
lsdb = {}        # ex: { "R1": {"R2": 4}, "R2": {"R1": 4, "R3": 1} }

# === RECEBER PACOTES ===
def escutar():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", PORTA_BASE + int(ID[1:])))
    while True:
        data, addr = sock.recvfrom(4096)
        pacote = json.loads(data.decode())
        tratar_pacote(pacote)

# === ENVIAR HELLO e LSA ===
def anunciar():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        lsa = {
            "tipo": "LSA",
            "origem": ID,
            "vizinhos": vizinhanca
        }
        msg = json.dumps(lsa).encode()
        for vizinho in vizinhanca:
            porta = PORTA_BASE + int(vizinho[1:])
            sock.sendto(msg, ("localhost", porta))
        time.sleep(10)

# === PROPAGAR LSA ===
def propagar_lsa(pacote):
    msg = json.dumps(pacote).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for vizinho in vizinhanca:
        porta = PORTA_BASE + int(vizinho[1:])
        sock.sendto(msg, ("localhost", porta))

# === DIJKSTRA ===
def dijkstra(origem):
    dist = defaultdict(lambda: float('inf'))
    anterior = {}
    dist[origem] = 0
    fila = [(0, origem)]

    while fila:
        custo, atual = heapq.heappop(fila)
        if atual not in lsdb:
            continue
        for viz, peso in lsdb[atual].items():
            novo_custo = custo + peso
            if novo_custo < dist[viz]:
                dist[viz] = novo_custo
                anterior[viz] = atual
                heapq.heappush(fila, (novo_custo, viz))

    print(f"\n[{ID}] Tabela de Roteamento:")
    for destino in sorted(dist.keys()):
        if destino == origem:
            continue
        caminho = [destino]
        while caminho[-1] != origem:
            caminho.append(anterior.get(caminho[-1], origem))
        caminho.reverse()
        print(f"Destino: {destino} | Custo: {dist[destino]} | Caminho: {' -> '.join(caminho)}")

# === TRATAR PACOTES ===
def tratar_pacote(pacote):
    global lsdb
    if pacote["tipo"] == "LSA":
        origem = pacote["origem"]
        vizinhos = pacote["vizinhos"]
        if origem not in lsdb or lsdb[origem] != vizinhos:
            print(f"[{ID}] LSA recebido de {origem}: {vizinhos}")
            lsdb[origem] = vizinhos
            propagar_lsa(pacote)
            dijkstra(ID)

# === MAIN ===
if __name__ == "__main__":
    print(f"[{ID}] Inicializando...")

    with open(f"./configs/config-{ID}.json", "r") as f:
        vizinhanca = json.load(f)

    print(f"[{ID}] Vizinhança: {vizinhanca}")

    # Iniciar threads
    threading.Thread(target=escutar, daemon=True).start()
    threading.Thread(target=anunciar, daemon=True).start()

    while True:
        time.sleep(1)
