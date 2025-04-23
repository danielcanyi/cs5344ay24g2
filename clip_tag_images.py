import os
import json
import torch
import open_clip
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

SOURCE_IMAGE_DIR = "data/images"
METADATA_OUTPUT_DIR = "data/clip_images"

# List of candidate tags
CANDIDATE_TAGS = [
    "hiking", "swimming", "sightseeing", "surfing", "eating street food",
    "shopping", "camping", "visiting temples", "exploring caves",
    "taking photos", "riding a boat", "attending a festival", 
    "sunbathing", "snorkeling", "biking", "rock climbing",
    "night market", "wildlife watching", "skiing", "kayaking"
]

def load_clip_model():
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
    tokenizer = open_clip.get_tokenizer('ViT-B-32')
    return model.eval().cuda(), preprocess, tokenizer

def tag_image(img_path, model, preprocess, tokenizer, candidate_tags):
    try:
        image = preprocess(Image.open(img_path).convert("RGB")).unsqueeze(0).cuda()
    except Exception as e:
        print(f"Failed to load image {img_path}: {e}")
        return []

    with torch.no_grad():
        image_features = model.encode_image(image)

        text_inputs = tokenizer(candidate_tags).cuda()
        text_features = model.encode_text(text_inputs)

        similarity = (image_features @ text_features.T).softmax(dim=-1).squeeze()
        topk = similarity.topk(5)

        tags = [candidate_tags[i] for i in topk.indices.tolist()]
        return tags

def save_metadata_json(output_path, key_terms):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"key_terms": key_terms}, f, ensure_ascii=False, indent=2)

def scan_and_tag_images():
    model, preprocess, tokenizer = load_clip_model()

    all_images = []
    for root, _, files in os.walk(SOURCE_IMAGE_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                all_images.append(full_path)

    print(f"Found {len(all_images)} images.")

    for img_path in tqdm(all_images, desc="Tagging images"):
        key_terms = tag_image(img_path, model, preprocess, tokenizer, CANDIDATE_TAGS)

        # Construct parallel .json path in clip_images/
        relative_path = os.path.relpath(img_path, SOURCE_IMAGE_DIR)
        json_path = os.path.join(METADATA_OUTPUT_DIR, relative_path + ".json")

        save_metadata_json(json_path, key_terms)

if __name__ == "__main__":
    scan_and_tag_images()