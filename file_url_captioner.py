from typing import Any

import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup, ResultSet, PageElement
from transformers import AutoProcessor, BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model: BlipForConditionalGeneration = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def find_captions(input_url: str):
    response = requests.get(input_url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_elements = soup.find_all("img")
    list_captions = elements_and_captions(img_elements)
    return "\n".join(list_captions)

def elements_and_captions(img_elements: ResultSet[PageElement]) -> list[Any] | None:
    output_with_captions = []
    for img_element in img_elements:
        img_url = img_element.get("src")
        if 'svg' in img_url or '1x1x' in img_url:
            continue

        if img_url.startswith("//"):
            img_url = f"https:{img_url}"
        elif not img_url.startswith("http://") and not img_url.startswith("https://"):
            continue

        try:
            response = requests.get(img_url)
            raw_image = Image.open(BytesIO(response.content))
            if raw_image.size[0] * raw_image.size[1] < 400:
                continue
            raw_image = raw_image.convert("RGB")
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)
            output_with_captions.append(f"{img_url}:{caption}")
        except Exception as e:
            print(f"Error processing image {img_url}: {e}")
            continue

    return output_with_captions


