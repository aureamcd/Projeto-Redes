FROM python:3.11-slim

# Instala dependências de rede e limpa cache para reduzir tamanho da imagem
RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    traceroute \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY host.py .
CMD ["python", "host.py"]