FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema para o Playwright
RUN apt-get update && apt-get install -y wget gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências do scraper
COPY scraper/requirements.txt ./scraper/requirements.txt
RUN pip install --upgrade pip && pip install -r scraper/requirements.txt && playwright install --with-deps

# Copia requirements e instala dependências do agent
COPY agent/requirements.txt ./agent/requirements.txt
RUN pip install -r agent/requirements.txt

# Copia todo o código do projeto
COPY . .

EXPOSE 8000