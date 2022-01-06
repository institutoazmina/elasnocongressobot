FROM python:3.6.15-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "sleep", "84000" ]