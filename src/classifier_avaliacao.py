from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer
import torch
from torch import cuda
import pandas as pd
import time

# Get the current date in YYYYMMDD format for file handling
current_date = time.strftime("%Y%m%d", time.localtime())

def get_device():
    """Detect the available device (CUDA or CPU)."""
    return 'cuda' if cuda.is_available() else 'cpu'

def load_model_and_tokenizer(model_name, device):
    """Load the pretrained model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.to(device)
    return model, tokenizer

def inference(model, tokenizer, class_mapping, input_text, device):
    """Perform inference on input text and return the classification result."""
    tokens = tokenizer(input_text, truncation=True, max_length=512, return_tensors="pt")
    tokens = {key: value.to(device) for key, value in tokens.items()}

    with torch.no_grad():
        outputs = model(**tokens)

    # Get the predicted probabilities
    probabilities = outputs.logits.softmax(dim=-1).tolist()[0]

    # Get the predicted class index
    predicted_index = torch.argmax(outputs.logits, dim=-1).item()

    # Map the index to the class label
    predicted_label = class_mapping[predicted_index]

    return predicted_label, probabilities

def process_row(row, model, tokenizer, class_mapping, device):
    """Process a single row to determine if the PL is favorable or not."""
    input_text = row.get('ementa') or row.get('Ementa', '')
    input_text = input_text.lower()  # Optional: Lowercase the text for consistency

    # Get the model's prediction
    predicted_label, probabilities = inference(model, tokenizer, class_mapping, input_text, device)

    # Add the prediction to the row
    row['classification'] = predicted_label
    row['probabilities'] = probabilities  # Optionally include probabilities for each class
    return row

if __name__ == "__main__":
    # Define device and model/tokenizer names
    DEVICE = get_device()
    MODEL_NAME = "belisards/ia-feminista-bert-posicao"

    # Load the model and tokenizer
    model, tokenizer = load_model_and_tokenizer(MODEL_NAME, DEVICE)

    # Load config to get class mapping (id2label)
    config = AutoConfig.from_pretrained(MODEL_NAME)
    class_mapping = config.id2label  # Maps index to class names (e.g., 0 -> 'favorável', 1 -> 'não favorável')

    # Define input and output files
    input_files = [f"senado_{current_date}.csv", f"camara_{current_date}.csv"]
    output_files = [f"senado_output_{current_date}.csv", f"camara_output_{current_date}.csv"]

    # Process each file
for input_file, output_file in zip(input_files, output_files):
    start_time = time.time()
    df = pd.read_csv(input_file)
    
    # Process each row in the DataFrame using apply
    df = df.apply(lambda row: process_row(row, model, tokenizer, class_mapping, DEVICE), axis=1)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    # Print processing details
    total_time = time.time() - start_time
    print(f"Processed {len(df)} rows and saved data to {output_file}")
    print(f"Total time taken: {total_time:.2f} seconds")

    # Print the most predicted values
    classification_counts = df['classification'].value_counts()
    print("Most predicted classification values:")
    print(classification_counts)
