import requests
from tkinter import *
from tkinter import ttk, messagebox

# -------------------- CONSTANTS --------------------
BASE_URL = "https://pokeapi.co/api/v2/"
FONT_TITLE = ("Times New Roman", 16, "bold")
FONT_BODY = ("Times New Roman", 12)

# -------------------- API FUNCTIONS --------------------
def fetch_pokemon(name):
    url = BASE_URL + "pokemon/" + name.lower()
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def fetch_ability(name):
    url = BASE_URL + "ability/" + name.lower()
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# -------------------- WINDOW HELPERS --------------------
def create_window(title, size="400x500"):
    win = Toplevel()
    win.title(title)
    win.geometry(size)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    frame = ttk.Frame(win, padding=15)
    frame.grid(sticky="nsew")
    frame.columnconfigure(0, weight=1)
    return win, frame

def scrollable_text(parent):
    text = Text(parent, wrap="word", font=FONT_BODY)
    scrollbar = ttk.Scrollbar(parent, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)

    text.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    parent.rowconfigure(1, weight=1)
    parent.columnconfigure(0, weight=1)
    return text

# -------------------- DISPLAY FUNCTIONS --------------------
def display_pokemon(name):
    data = fetch_pokemon(name)
    if not data:
        messagebox.showerror("Error", "Pokemon not found!")
        return

    win, frame = create_window("Pokemon Details")

    ttk.Label(frame, text="Pokemon Information", font=FONT_TITLE).grid(row=0, column=0, pady=10)

    text = scrollable_text(frame)
    text.insert(END, f"Name: {data['forms'][0]['name'].title()}\n")
    text.insert(END, f"ID: {data['id']}\n\n")

    text.insert(END, "Abilities:\n")
    for i, a in enumerate(data['abilities'], 1):
        hidden = "Yes" if a['is_hidden'] else "No"
        text.insert(END, f"  {i}. {a['ability']['name']} (Hidden: {hidden})\n")

    text.config(state="disabled")

def display_ability(name):
    data = fetch_ability(name)
    if not data:
        messagebox.showerror("Error", "Ability not found!")
        return

    win, frame = create_window("Ability Details")

    ttk.Label(frame, text="Ability Information", font=FONT_TITLE).grid(row=0, column=0, pady=10)

    text = scrollable_text(frame)
    text.insert(END, f"Name: {data['name'].title()}\n")
    text.insert(END, f"ID: {data['id']}\n\n")

    # Effect description (English only)
    for entry in data['effect_entries']:
        if entry['language']['name'] == 'en':
            text.insert(END, f"Description:\n{entry['effect']}\n\n")
            break

    text.insert(END, "Pokemon with this Ability:\n")
    for i, p in enumerate(data['pokemon'], 1):
        text.insert(END, f"  {i}. {p['pokemon']['name']}\n")

    text.config(state="disabled")

# -------------------- SEARCH WINDOWS --------------------
def pokemon_search():
    win, frame = create_window("Search Pokemon", "300x200")

    ttk.Label(frame, text="Enter Pokemon Name", font=FONT_TITLE).grid(row=0, column=0, pady=10)

    name_var = StringVar()
    ttk.Entry(frame, textvariable=name_var, font=FONT_BODY, justify="center").grid(row=1, column=0, pady=10)

    ttk.Button(
        frame,
        text="Search",
        command=lambda: display_pokemon(name_var.get())
    ).grid(row=2, column=0, pady=10)

def ability_search():
    win, frame = create_window("Search Ability", "300x200")

    ttk.Label(frame, text="Enter Ability Name", font=FONT_TITLE).grid(row=0, column=0, pady=10)

    ability_var = StringVar()
    ttk.Entry(frame, textvariable=ability_var, font=FONT_BODY, justify="center").grid(row=1, column=0, pady=10)

    ttk.Button(
        frame,
        text="Search",
        command=lambda: display_ability(ability_var.get())
    ).grid(row=2, column=0, pady=10)

# -------------------- MAIN WINDOW --------------------
root = Tk()
root.title("PokiSearch")
root.geometry("350x250")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main = ttk.Frame(root, padding=20)
main.grid(sticky="nsew")
main.columnconfigure(0, weight=1)

ttk.Label(main, text="Welcome to PokiSearch 😃", font=FONT_TITLE).grid(row=0, column=0, pady=15)

ttk.Button(main, text="Search Pokemon", command=pokemon_search).grid(row=1, column=0, pady=8)
ttk.Button(main, text="Search Ability", command=ability_search).grid(row=2, column=0, pady=8)
ttk.Button(main, text="Exit", command=root.quit).grid(row=3, column=0, pady=8)

root.mainloop()
