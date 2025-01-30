import torch
import logging
import pandas as pd
from typing import Any, Dict, Tuple
from pandas import Series
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    PreTrainedModel
)


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