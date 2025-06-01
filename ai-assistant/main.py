import sys
import os

# Add parent directory so `shared_func` becomes visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared_func.bedrock_func import *

from shared_func.polly_func import *

if __name__ == "__main__":


    if len(sys.argv) > 1 and sys.argv[1] == "1":
        speak = True
    else: 
        speak = False


    if speak:
        polly_speak(
            text = """Hey,Roberto!""", 
            voice_id="Kendra"
        )
    res = run_bedrock()

    if speak:
        polly_speak(
            text =res, 
            voice_id="Kendra"
        )
