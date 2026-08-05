# 1. Imagem base otimizada do Python (Slim para manter a imagem leve)
FROM python:3.10-slim

# 2. Configurações para otimizar a execução do Python em containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 3. Define o diretório de trabalho dentro do container
WORKDIR /app

# 4. Instala dependências do sistema necessárias para compilação (se preciso)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia primeiro os arquivos de dependência (aproveita a camada de cache do Docker)
COPY requirements.txt .

# 6. Instala as bibliotecas do Python sem guardar cache de instalação
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copia o código-fonte e o script principal de orquestração
COPY src/ ./src/
COPY main.py .

# 8. Comando que será executado quando o container rodar
CMD ["python", "main.py"]