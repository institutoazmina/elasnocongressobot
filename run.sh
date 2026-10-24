#!/bin/bash

# docker compose exec -T elasnacamera bash -c "cd src && python3 -m scrapy crawl camara"
docker compose exec -T elasnacamera bash -c "cd src && python3 -m scrapy crawl camara -a date_from=2025-04-13 -a date_to=2026-03-31"
docker compose exec -T elasnacamera bash -c "cd src && python3 -m scrapy crawl senado -a date_from=2025-04-13 -a date_to=2026-03-31"
# docker compose exec -T elasnacamera bash -c "cd src && python3 run_models.py"
# docker compose exec -T elasnacamera bash -c "cd src && python3 sync_spreadsheets.py"
