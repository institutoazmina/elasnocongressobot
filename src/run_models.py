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
    python run_models.py

Os arquivos de entrada devem seguir o padrão:
    senado_YYYYMMDD.csv
    camara_YYYYMMDD.csv

onde YYYYMMDD é a data atual.
"""
from torch import cuda  
import torch  
import pandas as pd  
import time, os  
import logging 
from typing import Dict  
from transformers import AutoConfig

# Custom functions
from utils_inteiroteor import textfrompdf, inference 
from utils_ementa import load_model_and_tokenizer, process_row_tema, process_row_posicao 

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
current_date = time.strftime("%Y%m%d", time.localtime())
DEVICE = 'cuda' if cuda.is_available() else 'cpu'
MODEL_NAME_TEMA = "azmina/ia_feminista_tema"
MODEL_NAME_POSICAO = "azmina/ia-feminista-bert-posicao"
TOKENIZER_NAME = "neuralmind/bert-base-portuguese-cased"

# Get env variables
from dotenv import load_dotenv
load_dotenv()
API_TOKEN = os.getenv('REPLICATE_KEY') 

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

        # Define input files
        files = [f"senado_{current_date}.csv", f"camara_{current_date}.csv"]

        for file in files:
            # Load input data
            logger.info(f"Processing file: {file}")
            df = pd.read_csv(file)

            # Process for `tema` columns
            logger.info("Processing tema classification")
            df = df.apply(lambda row: process_row_tema(row, model_tema, tokenizer_tema, class_mapping_tema, DEVICE, themes=THEMES), axis=1)

            # Process for `classification` columns
            logger.info("Processing position classification")
            df = df.apply(lambda row: process_row_posicao(row, model_class, tokenizer_class, class_mapping_class, DEVICE), axis=1)

            # Check if file startwith camara and token exists
            if file.startswith("camara"):
                # Process for `classification` columns
                logger.info("Getting text from PDF")
                df["texto"] = df["urlInteiroTeor"].apply(textfrompdf)
                logger.info("Classifying full text")
                df["posicao_llm"] = df["texto"].apply(lambda x: inference(x, API_TOKEN))
                # drop texto
                df.drop(columns=["texto"], inplace=True)

            # Save the updated DataFrame back to the same file
            df.to_csv(file, index=False)
            logger.info(f"Successfully processed {len(df)} rows in {file}")

    except Exception as e:
        logger.error(f"Critical error during execution: {str(e)}")
        raise
    finally:
        if DEVICE == 'cuda':
            torch.cuda.empty_cache()
            logger.info("CUDA cache cleared")