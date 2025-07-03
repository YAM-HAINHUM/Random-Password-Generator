import tkinter as tk
from tkinter import messagebox, ttk
import random
import string

# ------------------ Password Generator Logic ------------------ #
def generate_password(length, use_uppercase, use_numbers, use_symbols, exclude_chars):
    character_set = list(string.ascii_lowercase)

    if use_uppercase:
        character_set += list(string.ascii_uppercase)
    if use_numbers:
        character_set += list(string.digits)
    if use_symbols:
        character_set += list(string.punctuation)

    character_set = [ch for ch in character_set if ch not in exclude_chars]

    if not character_set:
        raise ValueError("No characters available for password generation.")

    password = []
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))

    password += [random.choice(character_set) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)

def check_strength(pwd):
    length = len(pwd)
    strength = 0
    if any(c.islower() for c in pwd): strength += 1
    if any(c.isupper() for c in pwd): strength += 1
    if any(c.isdigit() for c in pwd): strength += 1
    if any(c in string.punctuation for c in pwd): strength += 1

    if length >= 12 and strength == 4:
        return 'Strong', 'green', 300
    elif length >= 8 and strength >= 3:
        return 'Moderate', 'orange', 200
    else:
        return 'Weak', 'red', 100

# ------------------ GUI Events ------------------ #
def on_generate():
    try:
        length = int(length_entry.get())
        if length < 6:
            raise ValueError("Password must be at least 6 characters.")

        password = generate_password(
            length,
            uppercase_var.get(),
            numbers_var.get(),
            symbols_var.get(),
            exclude_entry.get()
        )

        result_var.set(password)
        password_entry.config(show="*" if not show_var.get() else "")
        password_listbox.insert(tk.END, password)

        strength_text, color, bar_width = check_strength(password)
        strength_label.config(text=f"Strength: {strength_text}", fg=color)
        strength_canvas.coords(strength_bar_rect, 0, 0, bar_width, 10)
        strength_canvas.itemconfig(strength_bar_rect, fill=color)

        copy_to_clipboard(password)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard.")

def toggle_password():
    password_entry.config(show="" if show_var.get() else "*")

def change_theme(event=None):
    theme = theme_var.get()
    colors = {
        "light": {"bg": "#dff6f9", "fg": "black", "entry_bg": "white"},
        "dark": {"bg": "#2e2e2e", "fg": "white", "entry_bg": "#4f4f4f"}
    }
    style = colors[theme]
    root.config(bg=style["bg"])
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type in ['Label', 'Button', 'Checkbutton']:
            widget.config(bg=style["bg"], fg=style["fg"])
        elif widget_type == 'Entry':
            widget.config(bg=style["entry_bg"], fg=style["fg"])
        elif widget_type == 'Listbox':
            widget.config(bg=style["entry_bg"], fg=style["fg"])
        elif widget_type == 'TCombobox':
            widget.configure(background=style["entry_bg"], foreground=style["fg"])

# ------------------ GUI Setup ------------------ #
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x500")

# Variables
result_var = tk.StringVar()
show_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
theme_var = tk.StringVar(value="light")

# Layout
tk.Label(root, text="Password Generator", font=("Arial", 14, "bold")).pack(pady=5)

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.insert(0, "16")
length_entry.pack()

tk.Checkbutton(root, text="Include Letters", state=tk.DISABLED).pack()
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).pack()
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack()
tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var).pack()

tk.Label(root, text="Exclude characters (e.g. O0l1):").pack()
exclude_entry = tk.Entry(root)
exclude_entry.pack()

tk.Button(root, text="Generate Password", command=on_generate).pack(pady=10)

password_entry = tk.Entry(root, textvariable=result_var, show="*", font=('Courier', 12), justify='center')
password_entry.pack(pady=5)

tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password).pack()

strength_label = tk.Label(root, text="Strength: ", font=('Arial', 10))
strength_label.pack()

# Strength bar using Canvas
strength_canvas = tk.Canvas(root, width=300, height=10, bg='white', highlightthickness=0)
strength_canvas.pack(pady=2)
strength_bar_rect = strength_canvas.create_rectangle(0, 0, 0, 10, fill='red')

tk.Label(root, text="Password History:").pack()
password_listbox = tk.Listbox(root, height=6, width=40)
password_listbox.pack()

tk.Label(root, text="Select Theme:").pack()
theme_dropdown = ttk.Combobox(root, values=["light", "dark"], textvariable=theme_var, state="readonly", width=10)
theme_dropdown.pack()
theme_dropdown.bind("<<ComboboxSelected>>", change_theme)

# Apply initial theme
change_theme()

root.mainloop()
