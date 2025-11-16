#!/usr/bin/env python3
import boto3
from PIL import ImageGrab
import io

try:
    # Get image from clipboard
    image = ImageGrab.grabclipboard()
    if image is None:
        print("No image found in clipboard")
        exit(1)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    # Use Textract
    textract = boto3.client('textract')
    response = textract.detect_document_text(Document={'Bytes': img_bytes})
    
    # Extract text
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            print(block['Text'])
            
except Exception as e:
    print(f"Error: {e}")
