import boto3
from botocore.exceptions import ClientError
import json
from colorama import Fore, Style, init
import os
from rich.console import Console
from rich.markdown import Markdown
import os

# Initialize colorama and rich
init(autoreset=True)
console = Console()


# Initialize colorama for styled output
init(autoreset=True)

# Hardcoded output path
output_filename = "/tmp/ai-assistant.txt"

def get_user_input():
    print(f"\n{Fore.CYAN}💬 What would you like to ask LLaMA today? (type 'exit' to quit)")
    return input(f"{Fore.YELLOW}> {Style.RESET_ALL}")

def format_llama_prompt(prompt):
    return f"""
<|begin_of_text|>
<|start_header_id|>user<|end_header_id|>
{prompt}
<|start_header_id|>assistant<|end_header_id|>
"""

def invoke_llama_model(prompt_text):
    model_id = "us.meta.llama4-scout-17b-instruct-v1:0"
    formatted_prompt = format_llama_prompt(prompt_text)

    payload = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 0.5
    }

    try:
        # Replace 'my-second-user' with your desired profile name
        session = boto3.Session(profile_name="iesb", region_name="us-east-1")
        client = session.client("bedrock-runtime")
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json"
        )
        model_response = json.loads(response['body'].read())
        return model_response.get("generation", "[No response generated 😕]")
    except ClientError as e:
        return f"{Fore.RED}💥 ERROR: Failed to invoke model:\n{e}"

def save_output_to_temp_file(text):
    try:
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"{Fore.LIGHTCYAN_EX}📁 Output saved to: {output_filename}")
    except Exception as e:
        print(f"{Fore.RED}⚠️ Failed to save output: {e}")


def run_bedrock(user_prompt=None):
    print(f"{Fore.GREEN}🤖 Welcome to LLaMA CLI Assistant! Ready to think, imagine, and solve with you.")
    if user_prompt is None:
        user_prompt = get_user_input()
    if user_prompt.strip().lower() == "exit":
        print(f"{Fore.MAGENTA}👋 Thanks for chatting with LLaMA. Until next time!")

    print(f"{Fore.BLUE}🧠 Thinking...\n")
    response = invoke_llama_model(user_prompt)

    print(f"{Fore.GREEN}📣 LLaMA Says:\n")
    console.print(Markdown(response))  # <-- Rich Markdown rendering here
    save_output_to_temp_file(response)

    print(f"{Fore.LIGHTBLACK_EX}" + "-" * 60)
    return response


