FROM python:3.6.15-slim

RUN useradd -m app
USER app

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD exec /bin/sh -c "trap : TERM INT; sleep 9999999999d & wait"
