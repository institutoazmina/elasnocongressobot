"""Script para classificação automática de proposições legislativas.

Este script processa proposições legislativas da Câmara e do Senado,
realizando duas classificações:

1. Classificação temática: identifica até dois temas principais da proposição,
   combinando regras baseadas em palavras-chave com modelos de ML.

2. Classificação de posição: determina se a proposição tem impacto
   positivo ou negativo para questões de gênero e direitos das mulheres.

3. Classificação de posição: baseado no inteiro teor (apenas para PLs da Câmara por ora), determina se a proposição tem impacto
    positivo ou negativo para questões de gênero e direitos das mulheres.

Os modelos utilizados são:
- Tema: azmina/ia_feminista_tema
- Posição: azmina/ia-feminista-bert-posicao

Requisitos:
- Python 3.7+
- PyTorch
- Transformers
- Pandas
- Arquivos CSV de entrada com coluna 'ementa' ou 'Ementa'

Uso:
    python run_models.py [--date YYYYMMDD]

Os arquivos de entrada (em DATA_DIR) seguem o padrão:
    senado_YYYYMMDD.csv
    camara_YYYYMMDD.csv

onde YYYYMMDD é a data informada em --date (padrão: hoje).

A saída é gravada ao lado, sem alterar a entrada:
    senado_YYYYMMDD_classificado.csv
    camara_YYYYMMDD_classificado.csv

Se a saída já existir, as proposições (por `id`) já classificadas são
reaproveitadas e apenas as novas são processadas.
"""
from torch import cuda
import torch
import pandas as pd
import time, os
import logging
import sys
import replicate
from tenacity import Retrying, wait_fixed, retry_if_exception_type, stop_after_attempt
from pathlib import Path
from transformers import AutoConfig

# Custom functions
from utils_inteiroteor import textfrompdf, inference
from utils_ementa import load_model_and_tokenizer, process_row_tema, process_row_posicao
from utils_df_validation import validate_columns
from data_paths import get_data_dir, get_log_dir, dataset_from_path, raw_path, classified_path, parse_args

# Configure logging
log_directory = get_log_dir()

current_date = time.strftime("%Y%m%d", time.localtime())
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False  # utils_ementa configura o root logger; evita mensagens duplicadas

# Remove any existing handlers
logger.handlers = []

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# File handler for general logs
general_log_file = log_directory / f'model_processing_{current_date}.log'
file_handler = logging.FileHandler(general_log_file)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# File handler for errors
error_log_file = log_directory / f'model_errors_{current_date}.log'
error_handler = logging.FileHandler(error_log_file)
error_handler.setFormatter(log_formatter)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

# Configuration
DEVICE = 'cuda' if cuda.is_available() else 'cpu'
MODEL_NAME_TEMA = "azmina/ia_feminista_tema"
MODEL_NAME_POSICAO = "azmina/ia-feminista-bert-posicao"
TOKENIZER_NAME = "neuralmind/bert-base-portuguese-cased"

# Get env variables
from dotenv import load_dotenv
load_dotenv()
API_TOKEN = os.getenv('REPLICATE_KEY')
MODEL = os.getenv('MODEL', 'meta/meta-llama-3-70b-instruct')
DATA_DIR = get_data_dir()
LLM_CHUNK_SIZE = 100  # linhas por lote; o CSV é salvo a cada lote

# Rule-based classification
THEMES = {
        "Lei Maria da Penha": "maria da penha, lei nº 11.340, 11340",
        "raça": "ação afirmativa, ações afirmativas, antirracista, antirracistas, cor da pele, cor de pele, etnia, etnias, étnica, étnicas, étnico, étnicos, \
                interseccionalidade, interseccionalidades, microagressão, microagressões, negra, negras, negritude, parda, pardas, perfilamento racial, política afirmativa,\
                políticas afirmativas, preta, pretas, quilombo, quilombola, quilombolas, quilombos, raça, raciais, racial, racismo, racista, racistas, reconhecimento facial",
        "clima": "acordo de paris, ambientais, ambiental, meio ambiente, aquecimento global, biodiversidade, biodiversidades, carbono, clima, climas,\
                 climática, climáticas, climático, climáticos, comunidades tradicionais, contribuições nacionalmente determinadas (ndcs), desastre natural, \
                desastres naturais, efeito estufa, eficiência energética, emissão de gases, emissões de gases, enchente, energia renovável, energias renováveis, \
                eventos extremos, floresta, florestal, florestas, infraestrutura urbana, plano de adaptação, planos de adaptação, planos de mitigação, poluição, \
                populações vulneráveis, recursos hídricos, reflorestamento, sustentável, florestais"
    }


if __name__ == "__main__":
    try:
        # Load models, tokenizers, and configurations
        logger.info("Loading models and tokenizers...")
        model_tema, tokenizer_tema = load_model_and_tokenizer(MODEL_NAME_TEMA, TOKENIZER_NAME, DEVICE)
        model_class, tokenizer_class = load_model_and_tokenizer(MODEL_NAME_POSICAO, TOKENIZER_NAME, DEVICE)

        config_tema = AutoConfig.from_pretrained(MODEL_NAME_TEMA)
        config_class = AutoConfig.from_pretrained(MODEL_NAME_POSICAO)
        class_mapping_tema = config_tema.id2label
        class_mapping_class = config_class.id2label

        args = parse_args("Classifica proposições (tema e posição) dos CSVs em DATA_DIR.")
        logger.info(f"DATA_DIR={DATA_DIR} date={args.date}")

        for dataset in ("senado", "camara"):
            file = raw_path(DATA_DIR, dataset, args.date)
            output_file = classified_path(DATA_DIR, dataset, args.date)
            logger.info(f"Processing file: {file}")

            # Skip processing if file doesn't exist
            if not file.exists():
                logger.warning(f"File {file} does not exist. Skipping...")
                continue

            # Skip processing if file is empty
            if file.stat().st_size == 0:
                logger.warning(f"File {file} is empty. Skipping...")
                continue

            df = pd.read_csv(file)
            df = validate_columns(df, dataset_from_path(file))

            def save(frame):
                # Write to a temp file first so a failure never leaves a truncated output
                tmp_file = output_file.with_suffix(".csv.tmp")
                frame.to_csv(tmp_file, index=False)
                os.replace(tmp_file, output_file)

            # Reuse tema/position results from a previous run
            reused = df.iloc[0:0]
            if output_file.exists() and output_file.stat().st_size > 0:
                previous = validate_columns(pd.read_csv(output_file), dataset)
                reused = previous[previous["classification"].notna() & previous["id"].isin(df["id"])]
                df = df[~df["id"].isin(reused["id"])]
                logger.info(f"Reusing {len(reused)} rows already classified in {output_file}")

            if not df.empty:
                # Process for `tema` columns
                logger.info(f"Processing tema classification ({len(df)} rows)")
                df = df.apply(lambda row: process_row_tema(row, model_tema, tokenizer_tema, class_mapping_tema, DEVICE, themes=THEMES), axis=1)

                # Process for `classification` columns
                logger.info("Processing position classification")
                df = df.apply(lambda row: process_row_posicao(row, model_class, tokenizer_class, class_mapping_class, DEVICE), axis=1)

            result = pd.concat([part for part in (reused, df) if not part.empty], ignore_index=True)
            save(result)

            # Full-text classification (Câmara only, requires token).
            # Only rows still without `posicao_llm` are sent; progress is saved per chunk.
            if dataset == "camara" and API_TOKEN:
                def safe_inference(text):
                    # Check for invalid text returned by textfrompdf
                    if not text or not isinstance(text, str) or text.startswith("Failed to download") or text.startswith("An error occurred") or text.startswith("URL is empty"):
                        logger.warning(f"Skipping inference due to invalid or empty text.")
                        return None # Return None to prevent error

                    try:
                        for attempt in Retrying(
                            stop=stop_after_attempt(3),
                            wait=wait_fixed(12),
                            retry=retry_if_exception_type(replicate.exceptions.ReplicateError)
                        ):
                            with attempt:
                                return inference(text, API_TOKEN, MODEL)
                    except Exception as e:
                        logger.error(f"Inference failed after all retries: {e}")
                        return None # Return None if all retries fail

                # Convert to numeric, coercing errors (like None) to NaN
                result["posicao_llm"] = pd.to_numeric(result["posicao_llm"], errors="coerce")
                pending = result.index[result["posicao_llm"].isna()]
                logger.info(f"Classifying full text for {len(pending)} rows")
                for start in range(0, len(pending), LLM_CHUNK_SIZE):
                    chunk = pending[start:start + LLM_CHUNK_SIZE]
                    texts = result.loc[chunk, "urlInteiroTeor"].apply(textfrompdf)
                    result.loc[chunk, "posicao_llm"] = pd.to_numeric(texts.apply(safe_inference), errors="coerce")
                    # The mean function ignores NaN values
                    result["classification_posicao_final"] = result[["probabilities", "posicao_llm"]].mean(axis=1)
                    save(result)
                    logger.info(f"LLM progress: {min(start + LLM_CHUNK_SIZE, len(pending))}/{len(pending)}")

            logger.info(f"Successfully processed {len(result)} rows into {output_file}")

    except Exception as e:
        logger.error(f"Critical error during execution: {str(e)}")
        raise
    finally:
        if DEVICE == 'cuda':
            torch.cuda.empty_cache()
            logger.info("CUDA cache cleared")
