import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import AutoProcessor, BlipForConditionalGeneration
import sys

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model: BlipForConditionalGeneration = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

url = "https://elpais.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

img_elements = soup.find_all("img")

with open("altStrings.txt", "w") as altStrings_file:
    for img_element in img_elements:
        img_url = img_element.get("src")
        if 'svg' in img_url or '1x1' in img_url:
            sys.stdout.write(f"{img_url} was too small. Skipping this.")
            continue

        if img_url.startswith("//"):
            img_url = f"https:{img_url}"
        elif not img_url.startswith("http://") and not img_url.startswith("https://"):
            sys.stdout.write(f"{img_url} might be invalid or spurious. Skipping this.")
            continue

        try:
            response = requests.get(img_url)
            raw_image = Image.open(BytesIO(response.content))
            if raw_image.size[0] * raw_image.size[1] < 400:
                sys.stdout.write(f"{img_url} image size was too small. Skipping this.")
                continue
            raw_image = raw_image.convert("RGB")
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)

            altStrings_file.write(f"{img_url}:{caption}\n")
        except Exception as e:
            print(f"Error processing image {img_url}: {e}")
            continue