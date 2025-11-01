import boto3
import json
import base64
import os
from datetime import datetime

def generate_images():
    # Switch between models easily
    model_id = "amazon.nova-canvas-v1:0"  # or "amazon.titan-image-generator-v1"
    
    bedrock = boto3.client('bedrock-runtime')
    
    prompt = input("Enter your image prompt: ")
    if len(prompt) > 512:
        prompt = prompt[:512]
        print(f"Prompt truncated to 512 characters: {prompt}")
    num_images = int(input("Number of images (1-5): "))
    
    body = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": num_images,
            "quality": "standard",
            "width": 1024,
            "height": 1024
        }
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        contentType="application/json"
    )
    
    result = json.loads(response['body'].read())
    
    save_dir = os.path.expanduser("~/Pictures/Bedrock")
    os.makedirs(save_dir, exist_ok=True)
    
    for i, image_data in enumerate(result['images']):
        image_bytes = base64.b64decode(image_data)
        filename = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png"
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        print(f"Image saved: {filepath}")

if __name__ == "__main__":
    generate_images()
