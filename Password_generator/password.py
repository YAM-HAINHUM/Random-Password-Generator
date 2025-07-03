import tkinter as tk
import random
import string
from tkinter import messagebox  # Import messagebox for displaying messages

def generate_password(length, use_uppercase, use_numbers, use_symbols):
    """Generate a random password based on user-defined criteria"""
    character_set = string.ascii_lowercase  # Start with lowercase letters

    if use_uppercase:
        character_set += string.ascii_uppercase  # Add uppercase letters
    if use_numbers:
        character_set += string.digits  # Add numbers
    if use_symbols:
        character_set += string.punctuation  # Add symbols

    # Generate a random password
    password = ''.join(random.choice(character_set) for _ in range(length))
    return password

def save_to_memory(password):
    """Save the generated password to a memory file"""
    with open("password_memory.txt", "a") as file:
        file.write(f"Generated Password: {password}\n")

def on_generate():
    """Handle the generate button click"""
    try:
        length = int(length_entry.get())
        use_uppercase = uppercase_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        password = generate_password(length, use_uppercase, use_numbers, use_symbols)
        result_label.config(text=f"Generated password: {password}")
        save_to_memory(password)  # Save to memory
        messagebox.showinfo("Saved", "Your generated password has been saved.")  # Show success message
    except ValueError:
        result_label.config(text="Please enter a valid number for length.")

# Create the main window
root = tk.Tk()
root.title("Password Generator")

# Create and place labels and entry fields
tk.Label(root, text="Password Length:").grid(row=0, column=0)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1)

# Checkboxes for options
uppercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var).grid(row=1, columnspan=2)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(row=2, columnspan=2)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(row=3, columnspan=2)

# Create and place the generate button
generate_button = tk.Button(root, text="Generate Password", command=on_generate)
generate_button.grid(row=4, columnspan=2)

# Label to display the result
result_label = tk.Label(root, text="")
result_label.grid(row=5, columnspan=2)

# Run the application
root.mainloop()
