import boto3
import os
import json
import os
import time
from shared_func.comprehend_translate_func import comprehend_text
from shared_func.comprehend_translate_func import translate_text
from shared_func.argv_parser import get_input


text = get_input("text:")

lang_code = comprehend_text(text=text)

# Translate English to Portuguese, non-English to English
if lang_code == 'en':
    res = translate_text(text, lang_code, 'pt')
else:
    res = translate_text(text, lang_code, 'en')

print("\nsource language:",lang_code)
print("text:",text)
print("text translated:",res)
