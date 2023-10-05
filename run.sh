#!/bin/bash

date >> logs/docker.elasnocongresso.log
cd src/
python3 -m scrapy crawl camara 1>> logs/crawl_camara.log 2>> logs/crawl_camara_.err.log;
python3 -m scrapy crawl senado 1>> logs/crawl_senado.log 2>> logs/crawl_senado_.err.log;
python sync_spreadsheet.py

