# Task  : Web Scraping & File System Manipulation
# Scrapes Hugging Face Vision Model docs and saves them locally.


import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin

BASE_URL = "https://huggingface.co"
START_URL = "https://huggingface.co/docs/transformers/index"
MAIN_FOLDER = "Vision_Models"

VISION_KEYWORDS = [
    "vision", "vit", "clip", "blip", "detr", "owlvit", "dinov2", "swin", "convnext", "beit", "perceiver"
]

def fetch_page(url):
    """Download HTML and return BeautifulSoup object."""
    res = requests.get(url, timeout=30)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def get_vision_models():
    """Return a static list of known Hugging Face vision model docs."""
    known_models = {
        "ViT": "https://huggingface.co/docs/transformers/model_doc/vit",
        "CLIP": "https://huggingface.co/docs/transformers/model_doc/clip",
        "BLIP": "https://huggingface.co/docs/transformers/model_doc/blip",
        "DETR": "https://huggingface.co/docs/transformers/model_doc/detr",
        "OWL-ViT": "https://huggingface.co/docs/transformers/model_doc/owlvit",
        "DINOv2": "https://huggingface.co/docs/transformers/model_doc/dinov2",
        "BEiT": "https://huggingface.co/docs/transformers/model_doc/beit",
        "ConvNeXT": "https://huggingface.co/docs/transformers/model_doc/convnext",
    }
    return [(k, v) for k, v in known_models.items()]


def save_model_docs(models):
    """Create folders and save documentation."""
    os.makedirs(MAIN_FOLDER, exist_ok=True)

    for name, url in tqdm(models, desc="Scraping Vision Models"):
        folder = os.path.join(MAIN_FOLDER, name.replace("/", "_"))
        os.makedirs(folder, exist_ok=True)

        try:
            soup = fetch_page(url)
            text = soup.get_text(separator="\n", strip=True)
            file_path = os.path.join(folder, f"{name.replace('/', '_')}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f" Error scraping {name}: {e}")

    print(f"\n Done! Check the '{MAIN_FOLDER}' folder for the scraped docs.")

def main():
    print(" Finding Vision Models on Hugging Face...")
    models = get_vision_models()
    print(f"Found {len(models)} potential vision models.")
    if not models:
        print(" No models found. The docs layout may have changed.")
    else:
        save_model_docs(models)

if __name__ == "__main__":
    main()
