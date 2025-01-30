FROM python:3.13-slim

RUN useradd -m app
USER app

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Ensure local bin is in PATH
ENV PATH="/home/app/.local/bin:${PATH}"

# Keep container running
CMD ["sleep", "infinity"]
