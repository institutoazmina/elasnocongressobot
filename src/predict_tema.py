from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer
import torch
from torch import cuda
import pandas as pd
import time

# Get the current YMD to access the correct CSV files.
current_date = time.strftime("%Y%m%d", time.localtime())

def get_device():
    return 'cuda' if cuda.is_available() else 'cpu'

def load_model_and_tokenizer(model_name, tokenizer_name, device):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.to(device)
    return model, tokenizer

def inference(model, tokenizer, class_mapping, input_text, device):
    tokens = tokenizer(input_text, truncation=True, max_length=512, return_tensors="pt")
    tokens = {key: value.to(device) for key, value in tokens.items()}

    with torch.no_grad():
        outputs = model(**tokens)

    all_proba = outputs.logits.softmax(dim=-1).tolist()[0]
    top_two_indices = sorted(range(len(all_proba)), key=lambda i: all_proba[i], reverse=True)[:2]
    top_two_classes = [class_mapping[idx] for idx in top_two_indices]

    return top_two_classes, all_proba

def process_row(row, model, tokenizer, class_mapping, device, themes):
    ementa = row.get('ementa') or row.get('Ementa')
    ementa = ementa.lower()
    tema_1 = None

    # Check for predefined themes
    for theme, keywords in themes.items():
        if any(keyword in ementa for keyword in keywords.split(", ")):
            tema_1 = theme
            break

    # If a predefined theme was found, set tema_2 using the model
    if tema_1:
        top_classes, _ = inference(model, tokenizer, class_mapping, ementa, device)
        tema_2 = top_classes[0]
    else:
        # If no predefined theme, use the model for both themes
        top_classes, _ = inference(model, tokenizer, class_mapping, ementa, device)
        tema_1, tema_2 = top_classes[0], top_classes[1]

    row['tema_1'] = tema_1
    row['tema_2'] = tema_2
    return row

if __name__ == "__main__":
    DEVICE = get_device()
    MODEL_NAME = "azmina/ia_feminista_tema"
    TOKENIZER_NAME = 'neuralmind/bert-base-portuguese-cased'

    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(MODEL_NAME, TOKENIZER_NAME, DEVICE)
    
    # Load config to get class mapping
    config = AutoConfig.from_pretrained(MODEL_NAME)
    class_mapping = config.id2label

    """"
    Define input and output files
    The input files used here are the output files from the spiders
    Thus they use the format "senado_YYYYMMDD.csv" and "camara_YYYYMMDD.csv"
    """
    input_files = [f"senado_{current_date}.csv", f"camara_{current_date}.csv"]
    output_files = ["../dados/senado.csv","../dados/camara.csv"]  
    
    # Define rule-based classification
    themes = {
        "Lei Maria da Penha": "maria da penha, lei nº 11.340, 11340",
        "raça": "ação afirmativa, ações afirmativas, antirracista, antirracistas, cor da pele, cor de pele, etnia, etnias, étnica, étnicas, étnico, étnicos, interseccionalidade, interseccionalidades, microagressão, microagressões, negra, negras, negritude, parda, pardas, perfilamento racial, política afirmativa, políticas afirmativas, preta, pretas, quilombo, quilombola, quilombolas, quilombos, raça, raciais, racial, racismo, racista, racistas, reconhecimento facial",
        "clima": "acordo de paris, ambientais, ambiental, meio ambiente, aquecimento global, biodiversidade, biodiversidades, carbono, clima, climas, climática, climáticas, climático, climáticos, comunidades tradicionais, contribuições nacionalmente determinadas (ndcs), desastre natural, desastres naturais, efeito estufa, eficiência energética, emissão de gases, emissões de gases, enchente, energia renovável, energias renováveis, eventos extremos, floresta, florestal, florestas, infraestrutura urbana, plano de adaptação, planos de adaptação, planos de mitigação, poluição, populações vulneráveis, recursos hídricos, reflorestamento, sustentável, florestais"
    }

    # Process each file
    for input_file, output_file in zip(input_files, output_files):
        start_time = time.time()
        df = pd.read_csv(input_file)
        
        # Process each row in the dataframe using apply
        df = df.apply(lambda row: process_row(row, model, tokenizer, class_mapping, DEVICE, themes), axis=1)

        # Save the updated dataframe to a new CSV file
        df.to_csv(output_file, index=False)

        # Print processing details
        total_time = time.time() - start_time
        print(f"Processed {len(df)} rows and saved data to {output_file}")
        print(f"Total time taken: {total_time:.2f} seconds")

        # Print the most predicted values
        tema_1_counts = df['tema_1'].value_counts()
        tema_2_counts = df['tema_2'].value_counts()
        print("Most predicted tema_1 values:")
        print(tema_1_counts)
        print("Most predicted tema_2 values:")
        print(tema_2_counts)
