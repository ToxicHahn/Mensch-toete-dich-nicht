import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def count_lines_without_comments(file_path):
    total_lines = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        in_docstring = False
        for line in file:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
            
            # Check for triple quotes (docstring start or end)
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.endswith('"""') or stripped.startswith("'''"):
                    continue
                if not in_docstring:  # Starting a docstring
                    in_docstring = True
                elif in_docstring:  # Ending a docstring
                    in_docstring = False
                continue

            # Skip lines within docstrings
            if in_docstring:
                continue
            
            # Skip single-line comments
            if stripped.startswith("#"):
                continue
            
            # Count the line if it's not a comment or docstring
            total_lines += 1

    return total_lines

def open_file():
    file_path = filedialog.askopenfilename(
        title="Wähle eine Python-Datei",
        filetypes=(("Python-Dateien", "*.py"), ("Alle Dateien", "*.*"))
    )
    
    if file_path:
        try:
            # Anzahl der Codezeilen zählen
            total_lines = count_lines_without_comments(file_path)
            # Ergebnis anzeigen
            result_label.config(text=f"Anzahl der Codezeilen ohne Kommentare und Docstrings: {total_lines}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Es gab einen Fehler beim Lesen der Datei: {str(e)}")
    else:
        messagebox.showwarning("Warnung", "Keine Datei ausgewählt.")

# Tkinter-Fenster einrichten
root = tk.Tk()
root.title("Python Code Zeilen Zähler")
root.geometry("400x250")  # Setting a fixed window size
root.configure(bg="#f4f4f9")  # Light background color for modern look

# Set modern fonts and styles
font = ("Arial", 12)

# Frame for the content
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Title label
title_label = ttk.Label(frame, text="Zähler für Codezeilen", font=("Arial", 16, "bold"), anchor="center")
title_label.pack(pady=10)

# Button zum Öffnen einer Datei
open_button = ttk.Button(frame, text="Python-Datei auswählen", command=open_file, style="TButton")
open_button.pack(pady=10, ipadx=10, ipady=5)

# Result label for displaying the number of code lines
result_label = ttk.Label(frame, text="Anzahl der Codezeilen wird hier angezeigt.", wraplength=300, font=font)
result_label.pack()

# Set a modern button style
style = ttk.Style()
style.configure("TButton", 
                background="#4CAF50", 
                foreground="black", 
                font=("Arial", 12, "bold"),
                padding=10)

# Define the hover effect (button state)
style.map("TButton",
          foreground=[('pressed', 'black'), ('active', 'black')],
          background=[('pressed', '#45a049'), ('active', '#45a049')])

# GUI starten
root.mainloop()
