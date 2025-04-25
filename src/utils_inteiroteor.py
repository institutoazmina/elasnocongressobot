import replicate
from PyPDF2 import PdfReader
import os
import requests
import time
import logging
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log
)
logger = logging.getLogger(__name__)

def is_rate_limit_error(exception):
    return isinstance(exception, replicate.exceptions.ReplicateError) and getattr(exception, "status", None) == 429

def textfrompdf(url: str, filename: str = "downloaded_file.pdf") -> str:
    """
    Downloads a PDF from the given URL and extracts its text content.

    Parameters:
        url (str): The URL of the PDF to download. Must be a valid non-empty string.
        filename (str): The name of the temporary file to save the PDF. Defaults to "downloaded_file.pdf".

    Returns:
        str: The extracted text from the PDF or an error message.
    """
    if not url:
        return "URL is empty."

    try:
        # Step 1: Download the PDF using requests with headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response: requests.Response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the PDF to a file
        with open(filename, 'wb') as pdf_file:
            pdf_file.write(response.content)

        # Step 2: Extract text from the downloaded PDF
        with open(filename, 'rb') as pdf_file:
            reader: PdfReader = PdfReader(pdf_file)
            extracted_text: str = ""

            # Extract text from all pages
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                extracted_text += page.extract_text()

        # Remove the downloaded file
        os.remove(filename)
        return extracted_text

    except requests.RequestException as e:
        return f"Failed to download the PDF: {e}"
    except Exception as e:
        return f"An error occurred while reading the PDF: {e}"


@retry(
    retry=retry_if_exception(is_rate_limit_error),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=11, min=11, max=120),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def inference(prompt: str, api_token: str, model: str = "meta/meta-llama-3-70b-instruct") -> str:
    """
    Perform inference using the Replicate API.

    Parameters:
        prompt (str): The input prompt to classify.

    Returns:
        str: The classification result.

    Raises:
        EnvironmentError: If the api token environment variable is not set.
        ValueError: If the prompt is empty or invalid.
        replicate.exceptions.ReplicateError: If there is an error with the Replicate API.
    """
    # Validate the prompt
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string.")

    if not api_token:
        raise EnvironmentError("Please set the api token environment variable.")

    try:
        # Initialize the Replicate client
        replicate_client = replicate.Client(api_token=api_token)

        # Trim the prompt length to 8000 characters
        if len(prompt) > 8000:
            prompt = prompt[:8000]

        input_data = {
            "top_p": 0.9,
            "prompt": prompt,
            "min_tokens": 0,
            "temperature": 0.6,
            "prompt_template": """
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            \n\nClassify the following message. It is a law bill in Portuguese and you are a legal assistant defending the women's right. Answer only with 0 or 1. \
            Answer 0 if it supports womens rights and 1 if not. Answer only with the number and no justification.\
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            \n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
            \n\n""",
            "presence_penalty": 1.15
        }

        max_retries = 3
        retry_delay = 11
        attempt = 0
        output = ""

        while attempt < max_retries:
            try:
                for event in replicate_client.stream(model, input=input_data):
                    output += event.data
                break  # Success case
            except replicate.exceptions.ReplicateError as e:
                # Check for HTTP 429 status code
                if hasattr(e, 'status_code') and e.status_code == 429:
                    attempt += 1
                    if attempt < max_retries:
                        logger.warning(f"Rate limited (HTTP 429). Retrying in {retry_delay}s (attempt {attempt}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise replicate.exceptions.ReplicateError(
                            f"Failed after {max_retries} retries: {str(e)}"
                        )
                else:
                    raise  # Re-raise non-429 errors
            except Exception as e:
                raise  # Re-raise other exceptions

        # Remove empty curly braces from the output
        output = output.replace("{}", "")
        return output

    except replicate.exceptions.ReplicateError as e:
        raise replicate.exceptions.ReplicateError(f"Replicate API error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")