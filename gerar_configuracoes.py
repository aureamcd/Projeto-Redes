import json
import os

# Arquivo gerado na etapa 1
with open("topologia.json", "r") as f:
    arestas = json.load(f)

# Extrair os roteadores
roteadores = set()
for aresta in arestas:
    roteadores.add(aresta["origem"])
    roteadores.add(aresta["destino"])

# Criar pasta de configs se não existir
os.makedirs("configs", exist_ok=True)

# Inicializar configs
configs = {r: {} for r in roteadores}

# Preencher com vizinhos e custos
for aresta in arestas:
    origem = aresta["origem"]
    destino = aresta["destino"]
    custo = aresta["custo"]
    
    configs[origem][destino] = custo
    configs[destino][origem] = custo  # bidirecional

# Salvar cada config em um arquivo
for roteador, vizinhos in configs.items():
    with open(f"configs/config-{roteador}.json", "w") as f:
        json.dump(vizinhos, f, indent=4)

print("Arquivos de configuração por roteador gerados em ./configs/")
