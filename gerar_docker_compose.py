import json
import yaml

def gerar_docker_compose():
    with open("topologia.json", "r") as f:
        topologia = json.load(f)

    compose = {
        "version": "3.9",
        "services": {},
        "networks": {}
    }

    roteadores = set()
    for link in topologia:
        roteadores.add(link["origem"])
        roteadores.add(link["destino"])

    for r in roteadores:
        nome_roteador = r.lower()
        
        # Serviço do roteador
        compose["services"][nome_roteador] = {
            "build": "./roteador",
            "container_name": nome_roteador,
            "networks": [],
            "cap_add": ["NET_ADMIN"],
            "volumes": [
                "./configs:/app/configs"  # Montagem do volume para os roteadores
            ]
        }

        # Sub-rede exclusiva para hosts e roteador
        rede_hosts = f"{nome_roteador}_net"
        compose["networks"][rede_hosts] = {
            "driver": "bridge"
        }
        compose["services"][nome_roteador]["networks"].append(rede_hosts)

        # Cria os hosts do roteador
        for i in range(1, 3):
            host_name = f"host_{r[1:]}_{i}"
            compose["services"][host_name] = {
                "build": "./host",
                "container_name": host_name,
                "networks": [rede_hosts]
            }

    # Conectar roteadores entre si
    for link in topologia:
        r1 = link["origem"].lower()
        r2 = link["destino"].lower()
        rede_nome = f"{r1}_{r2}_net"
        
        compose["networks"][rede_nome] = {"driver": "bridge"}

        # Adiciona a rede compartilhada nos dois roteadores
        compose["services"][r1]["networks"].append(rede_nome)
        compose["services"][r2]["networks"].append(rede_nome)

    # Salva como docker-compose.yml
    with open("docker-compose.yml", "w") as f:
        yaml.dump(compose, f, sort_keys=False)

    print("Arquivo docker-compose.yml gerado com sucesso!")

if __name__ == "__main__":
    gerar_docker_compose()
