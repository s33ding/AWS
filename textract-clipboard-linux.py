#!/usr/bin/env python3
import boto3
import subprocess
import tempfile
import os

try:
    # Save clipboard image to temp file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        result = subprocess.run(['wl-paste', '--type', 'image/png'], stdout=tmp, check=True)
        tmp_path = tmp.name
    
    # Read image bytes
    with open(tmp_path, 'rb') as f:
        img_bytes = f.read()
    
    # Clean up temp file
    os.unlink(tmp_path)
    
    # Use Textract
    textract = boto3.client('textract')
    response = textract.detect_document_text(Document={'Bytes': img_bytes})
    
    # Extract text
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            print(block['Text'])
            
except subprocess.CalledProcessError:
    print("No image in clipboard or wl-paste failed")
except Exception as e:
    print(f"Error: {e}")
