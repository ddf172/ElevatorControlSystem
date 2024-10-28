# Używamy oficjalnego obrazu Pythona jako bazowego
FROM python:3.12-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Instalujemy potrzebne zależności
RUN apt-get update && \
    apt-get install -y python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Kopiujemy wymagania projektu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt