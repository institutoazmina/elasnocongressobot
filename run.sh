#!/bin/bash

D=$(date +%Y%m%d)   # fixa a data uma vez; evita virar a meia-noite entre as etapas
docker compose exec -T raspador bash -c "cd src && python3 -m scrapy crawl camara" &
docker compose exec -T raspador bash -c "cd src && python3 -m scrapy crawl senado" &
wait
docker compose exec -T raspador bash -c "cd src && python3 run_models.py --date $D"
docker compose exec -T raspador bash -c "cd src && python3 sync_spreadsheets.py --date $D"

# Backfill:
# docker compose exec -T raspador bash -c "cd src && python3 -m scrapy crawl camara -a date_from=2025-04-13 -a date_to=2026-03-31"
# docker compose exec -T raspador bash -c "cd src && python3 -m scrapy crawl senado -a date_from=2025-04-13 -a date_to=2026-03-31"

# Rodar uma data específica:
# docker compose exec -T raspador bash -c "cd src && python3 run_models.py --date 20261026"
# docker compose exec -T raspador bash -c "cd src && python3 sync_spreadsheets.py --date 20261026"
