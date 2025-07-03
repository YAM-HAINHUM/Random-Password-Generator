import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password(length, use_uppercase, use_numbers, use_symbols, exclude_chars):
    """Generate a secure password with the specified options."""
    character_set = list(string.ascii_lowercase)

    if use_uppercase:
        character_set += list(string.ascii_uppercase)
    if use_numbers:
        character_set += list(string.digits)
    if use_symbols:
        character_set += list(string.punctuation)

    # Remove excluded characters
    if exclude_chars:
        character_set = [ch for ch in character_set if ch not in exclude_chars]

    if not character_set:
        raise ValueError("No characters available for password generation.")

    # Ensure at least one character from each selected category is included (for strong password rule)
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


def save_to_memory(password):
    with open("password_memory.txt", "a") as file:
        file.write(f"Generated Password: {password}\n")


def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard.")


def on_generate():
    try:
        length = int(length_entry.get())
        if length < 6:
            raise ValueError("Password length must be at least 6 characters.")

        use_uppercase = uppercase_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()
        exclude_chars = exclude_entry.get()

        password = generate_password(length, use_uppercase, use_numbers, use_symbols, exclude_chars)
        result_label.config(text=f"Password: {password}")
        save_to_memory(password)
        copy_to_clipboard(password)
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))


# GUI setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x300")

# Input fields and labels
tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

uppercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

# Option checkboxes
tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var).pack()
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).pack()
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack()

# Exclude characters field
tk.Label(root, text="Exclude Characters (e.g. O0l1):").pack()
exclude_entry = tk.Entry(root)
exclude_entry.pack()

# Generate button
generate_button = tk.Button(root, text="Generate Password", command=on_generate)
generate_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()