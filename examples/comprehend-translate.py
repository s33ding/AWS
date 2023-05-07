import boto3
import os
import json
import os
import time
from shared_func.create_boto3_session_from_json import create_boto3_session
from shared_func.cloudwatch_func import create_log_group
from shared_func.argv_parser import get_input

# Read the AWS credentials from the JSON file
session = create_boto3_session()


# Initialize the Amazon Translate and Amazon Rekognition clients using the session
comprehend = session.client('comprehend')
translate = session.client('translate')


text_list = text_list = [
    'Hello, world!',                   # English
    'Bonjour, le monde!',              # French
    'Hola, mundo!',                    # Spanish
    'こんにちは、世界！',                 # Japanese
    '안녕하세요, 세상!',                    # Korean
    '你好，世界！',                        # Chinese (Simplified)
    'Привет, мир!',                     # Russian
    'Merhaba, dünya!',                  # Turkish
    'Ciao, mondo!',                     # Italian
    'Hallo, Welt!',                     # German
    'Hej, världen!',                    # Swedish
    'Bonjour tout le monde!',           # Haitian Creole
    'Salamu, dunia!',                   # Swahili
    'Hola, món!',                       # Catalan
    'Labas, pasauli!',                  # Lithuanian
    'Hei maailma!',                     # Finnish
    'Përshëndetje, botë!',               # Albanian
    'Բարեւ, աշխարհ!',                    # Armenian
    'Zdravstvuyte, mir!',                # Russian (formal)
    'Helo, byd!',                       # Welsh
    'Γειά σου, κόσμε!',                   # Greek
    'Hallo, werêld!',                   # Afrikaans
    'Moïen, Welt!',                     # Luxembourgish
    'Sawubona, Mhlaba!',                 # Zulu
    'Salam, dunyo!',                     # Uzbek
    'Sveika, pasaule!',                  # Latvian
    'Ahoj, světe!'                       # Czech 
    ]

# Translate each text sample in the list
for text in text_list:
    response = comprehend.detect_dominant_language(Text=text)

    # Extract the language code from the Comprehend response
    lang_code = response['Languages'][0]['LanguageCode']
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=lang_code, #there is an option for 'auto' 
        TargetLanguageCode='en'
    )

    print("\nsource language:",lang_code)
    print("text:",text)
    print("text translated:",response['TranslatedText'])
