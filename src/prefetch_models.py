"""Baixa para o cache do Hugging Face tudo o que run_models.py precisa.

Uso (rede necessária; o compose define HF_HUB_OFFLINE=1, então desligue-o):
    docker compose run --rm -e HF_HUB_OFFLINE=0 robo python3 src/prefetch_models.py

É idempotente: com o cache já preenchido termina em segundos.
Carrega os mesmos artefatos que run_models.py (modelo, tokenizer e config),
então o cache fica completo para execução offline.
"""
import os

# Precisa vir antes de importar transformers/huggingface_hub (lido na importação)
os.environ["HF_HUB_OFFLINE"] = "0"

from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer

from utils_ementa import MODEL_NAME_TEMA, MODEL_NAME_POSICAO, TOKENIZER_NAME

if __name__ == "__main__":
    AutoTokenizer.from_pretrained(TOKENIZER_NAME)
    for name in (MODEL_NAME_TEMA, MODEL_NAME_POSICAO):
        AutoConfig.from_pretrained(name)
        AutoModelForSequenceClassification.from_pretrained(name)
        print(f"ok: {name}")
    print(f"ok: {TOKENIZER_NAME}")
