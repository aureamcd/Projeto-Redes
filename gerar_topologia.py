# gerar_topologia.py
import networkx as nx
import json
import random
import matplotlib.pyplot as plt

def gerar_topologia(num_roteadores):
    # Gera um grafo pequeno-mundo parcialmente aleatório e conectado
    G = nx.connected_watts_strogatz_graph(n=num_roteadores, k=2, p=0.5)

    # Adiciona pesos (custos de enlace) aleatórios
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)

    # Converte para JSON
    topologia = []
    for u, v, data in G.edges(data=True):
        topologia.append({
            "origem": f"r{u}",
            "destino": f"r{v}",
            "custo": data['weight']
        })

    with open("topologia.json", "w") as f:
        json.dump(topologia, f, indent=4)

    print("Topologia salva em 'topologia.json'.")
    visualizar_topologia(G)


def visualizar_topologia(G):
    pos = nx.spring_layout(G, seed=42)  # Layout com espaçamento agradável
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    # Desenha os nós
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue")

    # Desenha as arestas
    nx.draw_networkx_edges(G, pos, width=2)

    # Desenha os rótulos dos nós
    labels = {i: f"r{i}" for i in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=12)

    # Desenha os pesos das arestas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Topologia da Rede (Grafo dos Roteadores)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    gerar_topologia(5)  # Você pode mudar o número de roteadores aqui
