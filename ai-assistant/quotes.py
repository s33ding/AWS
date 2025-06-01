import sys
import os
import random

# Add parent directory so `shared_func` becomes visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared_func.bedrock_func import *
from shared_func.polly_func import *
import tkinter as tk
import threading


import tkinter as tk
import threading
import textwrap
import os
from datetime import datetime


def show_popup(quote, sec=6):
    def close_after_delay():
        root.after(sec * 1000, root.destroy)

    def save_quote():
        save_dir = "/home/roberto/Github/Obsidian/s33ding/quotes"
        os.makedirs(save_dir, exist_ok=True)
        filename = datetime.now().strftime("quote_%Y%m%d_%H%M%S.txt")
        path = os.path.join(save_dir, filename)
        with open(path, "w") as f:
            f.write(quote)
        save_btn.config(text="Saved!", state="disabled", bg="#50fa7b")

    def close_popup():
        root.destroy()

    root = tk.Tk()
    root.title("Daily Quote")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="#282a36")  # Dracula background

    max_width = 600
    line_length = 80
    wrapped = textwrap.fill(quote, width=line_length)
    num_lines = wrapped.count('\n') + 1
    line_height = 26
    base_height = 140
    dynamic_height = base_height + num_lines * line_height

    # Create UI first
    frame = tk.Frame(root, bg="#44475a", bd=2, relief="solid")
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    label = tk.Label(
        frame,
        text=quote,
        wraplength=max_width - 50,
        font=("Georgia", 13, "italic"),
        bg="#44475a",
        fg="#f8f8f2",
        padx=20,
        pady=10,
        justify="center"
    )
    label.pack(expand=True, fill="both")

    btn_frame = tk.Frame(frame, bg="#44475a")
    btn_frame.pack(pady=(0, 10))

    save_btn = tk.Button(
        btn_frame,
        text="Save Quote",
        command=save_quote,
        font=("Helvetica", 10),
        bg="#6272a4",
        fg="#f8f8f2",
        activebackground="#bd93f9",
        relief="flat"
    )
    save_btn.pack(side="left", padx=10)

    close_btn = tk.Button(
        btn_frame,
        text="Close",
        command=close_popup,
        font=("Helvetica", 10),
        bg="#ff5555",
        fg="#f8f8f2",
        activebackground="#ff79c6",
        relief="flat"
    )
    close_btn.pack(side="left", padx=10)

    # Now update geometry and center
    root.update_idletasks()
    width = max_width
    height = dynamic_height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    threading.Thread(target=close_after_delay).start()
    root.mainloop()


quote_prompts = [
    "Give me a quote about persistence — just the quote and the author.",
    "Share a quote about personal growth, with the author’s name only.",
    "Give me a famous quote about hard work, and who said it.",
    "Show me a quote on resilience, along with the author.",
    "Give a quote about discipline — include only the author’s name.",
    "Share a quote about overcoming struggle, with attribution.",
    "Give me a quote on determination, and who said it.",
    "Provide a quote about meaningful work, plus the author.",
    "Show a quote on not giving up — just the words and who said them.",
    "Give me a short quote about steady effort, with the author’s name.",
    "Share a quote about lifelong learning, and the person who said it.",
    "Give me a quote about the value of consistency, with attribution.",
    "Provide a quote on pushing through difficulty — quote and author only.",
    "Show a quote about endurance from a historical figure — no explanation.",
    "Give me a quote about growth and progress — just the quote and author."
]

if __name__ == "__main__":
    speak = True

    # Pick a random quote prompt
    chosen_prompt = random.choice(quote_prompts)
    print(f"Prompt: {chosen_prompt}")

    # Add instruction to keep it concise
    instruction = "Respond with just one short quote and the author's name only. No explanations.\n"
    full_prompt = instruction + chosen_prompt

    # Pass the full prompt into the Bedrock function
    res = run_bedrock(full_prompt)

    if speak:
        polly_speak(
            text=res,
            voice_id="Kendra"
        )

    # Show quote in popup window
    show_popup(res)

