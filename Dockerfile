# Usa uma base Python leve
FROM python:3.10-slim

# Instala dependências de interface gráfica para o servidor
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos do seu projeto
COPY . .

# Instala as bibliotecas do requirements
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o sistema (Ajustaremos para Web em breve)
CMD ["python", "main.py"]
