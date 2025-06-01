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


def show_popup(quote, author, sec=6):
    def close_after_delay():
        root.after(sec * 1000, root.destroy)

    def save_quote():
        save_dir = "/home/roberto/Github/Obsidian/s33ding/quotes"
        os.makedirs(save_dir, exist_ok=True)
        quote_text = quote.strip()
        filename = f"{author}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt".replace(" ","_").lower()
        filename = filename.replace(" ","_").lower()

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
    "Give me a quote about persistence.",
    "Share a quote about personal growth.",
    "Give me a famous quote about hard work.",
    "Show me a quote on resilience.",
    "Give a quote about discipline.",
    "Share a quote about overcoming struggle.",
    "Give me a quote on determination.",
    "Provide a quote about meaningful work.",
    "Show a quote on not giving up.",
    "Give me a short quote about steady effort.",
    "Share a quote about lifelong learning.",
    "Give me a quote about the value of consistency.",
    "Provide a quote on pushing through difficulty.",
    "Show a quote about endurance from a historical figure.",
    "Give me a quote about growth and progress."
]

# List of 70 Western writers/philosophers and their countries
figures = [
    ("Socrates", "Greece"),
    ("Plato", "Greece"),
    ("Aristotle", "Greece"),
    ("Marcus Aurelius", "Italy"),
    ("Cicero", "Italy"),
    ("Seneca", "Spain"),
    ("Augustine of Hippo", "Algeria"),
    ("Boethius", "Italy"),
    ("Thomas Aquinas", "Italy"),
    ("Anselm of Canterbury", "England"),
    ("Michel de Montaigne", "France"),
    ("René Descartes", "France"),
    ("Francis Bacon", "England"),
    ("John Locke", "England"),
    ("David Hume", "Scotland"),
    ("Adam Smith", "Scotland"),
    ("Voltaire", "France"),
    ("Jean-Jacques Rousseau", "Switzerland"),
    ("Immanuel Kant", "Germany"),
    ("Leibniz", "Germany"),
    ("Hegel", "Germany"),
    ("Schopenhauer", "Germany"),
    ("Kierkegaard", "Denmark"),
    ("Nietzsche", "Germany"),
    ("Karl Marx", "Germany"),
    ("John Stuart Mill", "England"),
    ("Henrik Ibsen", "Norway"),
    ("Tolstoy", "Russia"),
    ("Dostoevsky", "Russia"),
    ("Whitman", "United States"),
    ("Emerson", "United States"),
    ("Bertrand Russell", "Wales"),
    ("Wittgenstein", "Austria"),
    ("Heidegger", "Germany"),
    ("Sartre", "France"),
    ("Simone de Beauvoir", "France"),
    ("Albert Camus", "Algeria"),
    ("Foucault", "France"),
    ("Derrida", "France"),
    ("Hannah Arendt", "Germany"),
    ("Isaiah Berlin", "Latvia"),
    ("Noam Chomsky", "United States"),
    ("Richard Rorty", "United States"),
    ("Cornel West", "United States"),
    ("José Ortega y Gasset", "Spain"),
    ("Gramsci", "Italy"),
    ("Umberto Eco", "Italy"),
    ("Jorge Luis Borges", "Argentina"),
    ("Octavio Paz", "Mexico"),
    ("García Márquez", "Colombia"),
    ("Vargas Llosa", "Peru"),
    ("Vaclav Havel", "Czech Republic"),
    ("Czesław Miłosz", "Poland"),
    ("Copernicus", "Poland"),
    ("Spinoza", "Netherlands"),
    ("Erasmus", "Netherlands"),
    ("Benedetto Croce", "Italy"),
    ("Giambattista Vico", "Italy"),
    ("Paul Tillich", "Germany"),
    ("Alasdair MacIntyre", "Scotland"),
    ("Charles Taylor", "Canada"),
    ("Gilles Deleuze", "France"),
    ("Slavoj Žižek", "Slovenia"),
    ("Karl Popper", "Austria"),
    ("Thomas Paine", "England"),
    ("Terry Eagleton", "England"),
    ("Herbert Marcuse", "Germany"),
    ("Hans-Georg Gadamer", "Germany"),
    ("Maurice Merleau-Ponty", "France")
]




if __name__ == "__main__":
    speak = True

    chosen_prompt = random.choice(quote_prompts)
    chosen_figure = random.choice(figures)
    author, country = chosen_figure


    print(f"Prompt: {chosen_prompt}")

    instruction = (
    f"Give me one very short, clear motivational quote (no more than 20 words) "
    f"by {author}, related to work, discipline, or progress. "
    f"Only return the quote and author's name. The author is from {country}."
)



    full_prompt = instruction + "\n" + chosen_prompt


    # Get the quote from the model
    res = run_bedrock(full_prompt)

    if speak:
        polly_speak(
            text=res,
            voice_id="Kendra"
        )

    # Show quote in popup
    show_popup(res,author)
