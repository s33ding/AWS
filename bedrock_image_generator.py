import boto3
import json
import base64
import os
import random
from datetime import datetime

def generate_images():
    model_id = "stability.stable-diffusion-xl-v1"

    session = boto3.Session(profile_name='iesb')
    bedrock = session.client('bedrock-runtime', region_name='us-east-1')

    prompt = input("Enter your image prompt: ")
    num_images = int(input("Number of images (1-5): "))

    body = json.dumps({
        "text_prompts": [
            {"text": prompt, "weight": 1.0},
            {"text": "blurry, low quality, cartoon, drawing, illustration, painting", "weight": -1.0}
        ],
        "cfg_scale": 7,
        "steps": 50,
        "seed": random.randint(0, 2147483647),
        "width": 1024,
        "height": 1024,
        "samples": num_images,
        "style_preset": "photographic"
    })

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        contentType="application/json"
    )

    result = json.loads(response['body'].read())

    save_dir = os.path.expanduser("~/Pictures/Bedrock")
    os.makedirs(save_dir, exist_ok=True)

    for i, artifact in enumerate(result['artifacts']):
        image_bytes = base64.b64decode(artifact['base64'])
        filename = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        print(f"Image saved: {filepath}")

if __name__ == "__main__":
    generate_images()
