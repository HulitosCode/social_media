FROM python:3.12-slim

# Desativa a criação de ambientes virtuais no Poetry para usar o ambiente global
ENV POETRY_VIRTUALENVS_CREATE=false

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos para o diretório de trabalho
COPY . .

# Instala o Poetry
RUN pip install poetry

# Configura o Poetry e instala as dependências sem interação e com saída limpa
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

# Expõe a porta 8000 para a aplicação
EXPOSE 8000

# Comando para iniciar a aplicação com o caminho correto para o arquivo main.py
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
