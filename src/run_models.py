from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer, PreTrainedModel
import torch
from torch import cuda
import pandas as pd
from pandas import DataFrame, Series
import time
import logging
from typing import Dict, List, Tuple, Optional, Any

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

def load_model_and_tokenizer(
    model_name: str,
    tokenizer_name: str,
    device: str
) -> Tuple[PreTrainedModel, Any]:
    """Load pre-trained model and tokenizer.
    
    Args:
        model_name: HuggingFace model identifier
        tokenizer_name: HuggingFace tokenizer identifier
        device: Device to load the model to ('cuda' or 'cpu')
    
    Returns:
        Tuple containing the loaded model and tokenizer
    
    Raises:
        Exception: If model or tokenizer loading fails
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.to(device)
        logger.info(f"Successfully loaded model {model_name}")
        return model, tokenizer
    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {str(e)}")
        raise

def process_row_tema(
    row: Series,
    model: PreTrainedModel,
    tokenizer: Any,
    class_mapping: Dict[int, str],
    device: str,
    themes: Dict[str, str]
) -> Series:
    """Process a single row for tema classification.
    
    Args:
        row: DataFrame row containing 'ementa' or 'Ementa' column
        model: Pre-trained classification model
        tokenizer: Tokenizer for the model
        class_mapping: Mapping from class indices to labels
        device: Device to run inference on
        themes: Dictionary of themes and their keywords
    
    Returns:
        Modified row with 'tema_1' and 'tema_2' columns added
    """
    ementa = row.get('ementa') or row.get('Ementa', '')
    ementa = ementa.lower()

    # Rule-based classification
    matching_themes = [
        theme for theme, keywords in themes.items()
        if any(keyword in ementa for keyword in keywords.split(", "))
    ]

    tokens = tokenizer(ementa, truncation=True, max_length=512, return_tensors="pt")
    tokens = {key: value.to(device) for key, value in tokens.items()}
    with torch.no_grad():
        outputs = model(**tokens)
    all_proba = outputs.logits.softmax(dim=-1).tolist()[0]
    top_two_indices = sorted(range(len(all_proba)), key=lambda i: all_proba[i], reverse=True)[:2]
    top_classes = [class_mapping[idx] for idx in top_two_indices]

    # Determine tema_1 and tema_2
    if len(matching_themes) >= 2:
        tema_1, tema_2 = matching_themes[:2]
    elif len(matching_themes) == 1:
        tema_1 = matching_themes[0]
        tema_2 = top_classes[0] if tema_1 != top_classes[0] else top_classes[1]
    else:
        tema_1, tema_2 = top_classes[0], top_classes[1]

    row['tema_1'] = tema_1
    row['tema_2'] = tema_2
    return row

def process_row_posicao(
    row: Series,
    model: PreTrainedModel,
    tokenizer: Any,
    class_mapping: Dict[int, str],
    device: str
) -> Series:
    """Process a single row for position classification.
    
    Args:
        row: DataFrame row containing 'ementa' or 'Ementa' column
        model: Pre-trained classification model
        tokenizer: Tokenizer for the model
        class_mapping: Mapping from class indices to labels
        device: Device to run inference on
    
    Returns:
        Modified row with 'classification' and 'probabilities' columns added
    """
    ementa = row.get('ementa') or row.get('Ementa', '').lower()

    tokens = tokenizer(ementa, truncation=True, max_length=512, return_tensors="pt")
    tokens = {key: value.to(device) for key, value in tokens.items()}
    with torch.no_grad():
        outputs = model(**tokens)
    probabilities = outputs.logits.softmax(dim=-1).tolist()[0]
    prob_positive = probabilities[1]
    predicted_index = torch.argmax(outputs.logits, dim=-1).item()
    predicted_label = class_mapping[predicted_index]

    row['classification'] = predicted_label
    row['probabilities'] = round(prob_positive, 2)
    return row

def process_file(
    input_file: str,
    output_file: str,
    model: PreTrainedModel,
    tokenizer: Any,
    class_mapping: Dict[int, str],
    device: str,
    process_row_func: Any,
    **kwargs: Any
) -> None:
    """Process an entire file applying the specified row processing function.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        model: Pre-trained classification model
        tokenizer: Tokenizer for the model
        class_mapping: Mapping from class indices to labels
        device: Device to run inference on
        process_row_func: Function to process each row
        **kwargs: Additional arguments passed to process_row_func
    """
    df = pd.read_csv(input_file)
    df = df.apply(lambda row: process_row_func(row, model, tokenizer, class_mapping, device, **kwargs), axis=1)
    df.to_csv(output_file, index=False)
    logger.info(f"Processed {len(df)} rows and saved to {output_file}")

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
        input_files = [f"senado_{current_date}.csv", f"camara_{current_date}.csv"]

        for file in input_files:
            # Load input data
            logger.info(f"Processing file: {file}")
            df = pd.read_csv(file)

            # Process for `tema` columns
            logger.info("Processing tema classification")
            df = df.apply(lambda row: process_row_tema(row, model_tema, tokenizer_tema, class_mapping_tema, DEVICE, themes=THEMES), axis=1)

            # Process for `classification` columns
            logger.info("Processing position classification")
            df = df.apply(lambda row: process_row_posicao(row, model_class, tokenizer_class, class_mapping_class, DEVICE), axis=1)

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