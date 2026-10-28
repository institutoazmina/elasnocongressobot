FROM python:3.13-slim

RUN useradd -m app
USER app

# Scripts instalados com `pip install --user` vão para /home/app/.local/bin;
# definido antes do pip para ele não avisar que o diretório está fora do PATH.
ENV PATH="/home/app/.local/bin:${PATH}"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório do cache do Hugging Face com o dono certo: um volume nomeado
# vazio herda o dono da imagem; sem isso ele nasce como root e o usuário app
# não consegue gravar nele.
RUN mkdir -p /home/app/.cache/huggingface

# Keep container running
CMD ["sleep", "infinity"]
