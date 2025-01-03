from tkinter import Tk, filedialog, messagebox, Frame, Button, Label
from tkinter import ttk
import ast

def generate_getters_setters_code(cls_name, init_params):
    # Code für Getter und Setter im camelCase-Stil generieren
    code = ""
    for attribute in init_params:
        # Getter-Methode im camelCase-Stil
        getter_code = f"    def hole{attribute.capitalize()}(self):\n"
        getter_code += f'        """Gibt {attribute} zurueck."""\n'        
        getter_code += f"        return self._{attribute}\n"
        
        # Setter-Methode im camelCase-Stil
        setter_code = f"    def setze{attribute.capitalize()}(self, value):\n"
        setter_code += f'        """Setzt {attribute}."""\n'    
        setter_code += f"        self._{attribute} = value\n"
        
        # Zusammenführen
        code += getter_code + "\n" + setter_code + "\n"
    
    return code


def process_python_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Versuchen, den Inhalt der Datei zu parsen
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        messagebox.showerror("Fehler", f"Fehler beim Parsen der Datei: {e}")
        return

    # Finden von Klassen in der Datei
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]

    class_code_changes = {}

    # Generieren der Getter und Setter für jede Klasse
    for class_node in classes:
        class_name = class_node.name
        init_method = None

        # Suchen der __init__ Methode in der Klasse
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                init_method = node
                break

        if init_method:
            # Extrahieren der Parameter der __init__-Methode
            init_params = [param.arg for param in init_method.args.args if param.arg != 'self']
            getter_setter_code = generate_getters_setters_code(class_name, init_params)
            class_code_changes[class_name] = getter_setter_code

    # Wenn Änderungen vorgenommen wurden, die Datei aktualisieren
    if class_code_changes:
        updated_content = content
        for class_name, getter_setter_code in class_code_changes.items():
            class_start = updated_content.find(f"class {class_name}")
            if class_start != -1:
                class_end = updated_content.find("class ", class_start + 1)
                if class_end == -1:
                    class_end = len(updated_content)
                class_body = updated_content[class_start:class_end]
                updated_content = updated_content.replace(class_body, class_body + "\n" + getter_setter_code)

        with open(file_path, "w") as file:
            file.write(updated_content)
        
        messagebox.showinfo("Erfolg", "Getter und Setter wurden erfolgreich zur Datei hinzugefügt!")


# GUI mit Tkinter
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Dateien", "*.py")])
    
    if file_path:
        process_python_file(file_path)

def create_gui():
    window = Tk()
    window.title("Getter und Setter Generator")
    window.geometry("400x250")
    window.configure(bg="#f0f0f0")  # Light background color

    # Set modern fonts
    font = ("Arial", 12)

    # Frame for the content
    frame = ttk.Frame(window, padding="20")
    frame.pack(fill="both", expand=True)

    # Title label
    title_label = ttk.Label(frame, text="Python Getter & Setter Generator", font=("Arial", 16, "bold"), anchor="center")
    title_label.pack(pady=10)

    # Button zum Öffnen einer Datei
    open_button = ttk.Button(frame, text="Python-Datei Öffnen", command=open_file, style="TButton")
    open_button.pack(pady=20, ipadx=10, ipady=5)

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

    window.mainloop()

# Anwendung starten
if __name__ == "__main__":
    create_gui()
