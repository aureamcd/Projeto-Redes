import threading
import time
import socket
import json
import os
from collections import defaultdict
import heapq

ID = os.getenv("ID")  # ID do roteador, vindo da variável de ambiente
PORTA_BASE = 5000

vizinhanca = {}  # { "R1": custo }
lsdb = {}        # { "R1": {"R2": 3, "R5": 6} }

# ==== RECEBER PACOTES ====
def escutar():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORTA_BASE + int(ID[1:])))
    while True:
        data, addr = sock.recvfrom(4096)
        pacote = json.loads(data.decode())
        tratar_pacote(pacote)

# ==== ENVIAR HELLO e LSA periodicamente ====
def anunciar():
    while True:
        # Enviar pacote LSA
        lsa = {
            "tipo": "LSA",
            "origem": ID,
            "vizinhos": vizinhanca
        }
        msg = json.dumps(lsa).encode()
        for vizinho in vizinhanca:
            porta = PORTA_BASE + int(vizinho[1:])
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(msg, (vizinho, porta))
        time.sleep(10)

# ==== TRATAR PACOTES ====
def tratar_pacote(pacote):
    global lsdb
    if pacote["tipo"] == "LSA":
        origem = pacote["origem"]
        vizinhos = pacote["vizinhos"]
        if origem not in lsdb or lsdb[origem] != vizinhos:
            print(f"[{ID}] LSA recebido de {origem}: {vizinhos}")
            lsdb[origem] = vizinhos
            # TODO: Propagar para vizinhos e rodar Dijkstra()

if __name__ == "__main__":
    print(f"[{ID}] Inicializando...")

    # TODO: Carregar vizinhos a partir de arquivo de configuração por container
    # Exemplo (depois): vizinhanca = {"R2": 4, "R3": 8}
# Carregar config
with open(f"./configs/config-{ID}.json", "r") as f:
    vizinhanca = json.load(f)
    
    # Iniciar threads
    t1 = threading.Thread(target=escutar)
    t2 = threading.Thread(target=anunciar)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
