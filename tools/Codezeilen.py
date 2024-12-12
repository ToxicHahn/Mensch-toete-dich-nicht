import tkinter as tk
from tkinter import filedialog, messagebox

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
            print(line)
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

# Layout
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

open_button = tk.Button(frame, text="Python-Datei auswählen", command=open_file)
open_button.pack(pady=10)

result_label = tk.Label(frame, text="Anzahl der Codezeilen wird hier angezeigt.", wraplength=300)
result_label.pack()

# GUI starten
root.mainloop()
