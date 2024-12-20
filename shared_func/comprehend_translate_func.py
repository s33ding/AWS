import boto3 

def comprehend_text(text):
    """
    Detects the dominant language of the input text using Amazon Comprehend
    
    Args:
    - text (str): the input text to be analyzed
    
    Returns:
    - lang_code (str): the language code of the detected language
    """
    comprehend = boto3.client('comprehend')
    
    # Detect the dominant language of the input text
    response = comprehend.detect_dominant_language(Text=text)
    
    # Extract the language code from the Comprehend response
    lang_code = response['Languages'][0]['LanguageCode']
    
    return lang_code

def translate_text(text, lang_code, target_lang_code='en'):
    """
    Translates the input text to English using Amazon Translate
    
    Args:
    - text (str): the input text to be translated
    - lang_code (str): the language code of the input text
    
    Returns:
    - translated_text (str): the translated text
    """
    translate = boto3.client('translate')
    
    # Translate the input text to English
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=lang_code,
        TargetLanguageCode=target_lang_code
    )
    
    # Extract the translated text from the Translate response
    translated_text = response['TranslatedText']
    
    return translated_text

