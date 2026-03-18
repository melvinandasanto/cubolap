import tkinter as tk
from tkinter import font

class FormularioOLAP:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis OLAP")
        self.root.geometry("500x500")
        
        # Color de fondo principal (Azul muy oscuro)
        self.bg_color = "#121f2d" 
        # Color del contenedor (Gris azulado oscuro)
        self.card_color = "#1e2d3e"
        # Color de los campos de texto
        self.entry_bg = "#2a3b4d"
        # Color del botón (Azul brillante)
        self.btn_color = "#4a90e2"
        
        self.root.configure(bg=self.bg_color)

        # Contenedor central (Frame)
        self.container = tk.Frame(self.root, bg=self.card_color, padx=40, pady=40, highlightbackground="#34495e", highlightthickness=1)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        # Tipografías
        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=10)
        self.btn_font = font.Font(family="Segoe UI", size=11, weight="bold")

        # Título
        tk.Label(self.container, text="SISTEMA DE ANÁLISIS OLAP", fg="white", bg=self.card_color, font=self.title_font).pack(pady=(0, 5))
        

        # Campo Usuario
        tk.Label(self.container, text="Usuario", fg="white", bg=self.card_color, font=self.label_font).pack(anchor="w")
        self.user_entry = tk.Entry(self.container, bg=self.entry_bg, fg="white", insertbackground="white", borderwidth=0, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x", pady=(5, 20), ipady=8)

        # Campo Contraseña
        tk.Label(self.container, text="Contraseña", fg="white", bg=self.card_color, font=self.label_font).pack(anchor="w")
        self.pass_entry = tk.Entry(self.container, bg=self.entry_bg, fg="white", insertbackground="white", borderwidth=0, font=("Segoe UI", 12), show="•")
        self.pass_entry.pack(fill="x", pady=(5, 30), ipady=8)

        # Botón Iniciar Sesión
        self.btn_login = tk.Button(self.container, text="Iniciar Sesión", bg=self.btn_color, fg="white", 
                                   activebackground="#357abd", activeforeground="white",
                                   font=self.btn_font, borderwidth=0, cursor="hand2")
        self.btn_login.pack(fill="x", ipady=10)

        # --- Sección de Estado Inferior ---
        self.footer = tk.Frame(self.container, bg=self.card_color)
        self.footer.pack(fill="x", pady=(30, 0))

      
        

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioOLAP(root)
    root.mainloop()