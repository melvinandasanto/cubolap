import tkinter as tk
from tkinter import font
from claseLogin import Autenticacion
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis OLAP")
        self.root.geometry("500x500")
        
        self.bg_color = "#121f2d"
        self.card_color = "#1e2d3e"
        self.entry_bg = "#2a3b4d"
        self.btn_color = "#4a90e2"
        
        self.root.configure(bg=self.bg_color)

        self.container = tk.Frame(self.root, bg=self.card_color, padx=40, pady=40, highlightbackground="#34495e", highlightthickness=1)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=10)
        self.btn_font = font.Font(family="Segoe UI", size=11, weight="bold")

        tk.Label(self.container, text="SISTEMA DE ANÁLISIS OLAP", fg="white", bg=self.card_color, font=self.title_font).pack(pady=(0, 5))

        tk.Label(self.container, text="Usuario", fg="white", bg=self.card_color, font=self.label_font).pack(anchor="w")
        self.user_entry = tk.Entry(self.container, bg=self.entry_bg, fg="white", insertbackground="white", borderwidth=0, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x", pady=(5, 20), ipady=8)

        tk.Label(self.container, text="Contraseña", fg="white", bg=self.card_color, font=self.label_font).pack(anchor="w")
        self.pass_entry = tk.Entry(self.container, bg=self.entry_bg, fg="white", insertbackground="white", borderwidth=0, font=("Segoe UI", 12), show="•")
        self.pass_entry.pack(fill="x", pady=(5, 30), ipady=8)

        self.btn_login = tk.Button(
            self.container,
            text="Iniciar Sesión",
            bg=self.btn_color,
            fg="white",
            activebackground="#357abd",
            activeforeground="white",
            font=self.btn_font,
            borderwidth=0,
            cursor="hand2",
            command=self.iniciar_sesion
        )
        self.btn_login.pack(fill="x", ipady=10)

        self.footer = tk.Frame(self.container, bg=self.card_color)
        self.footer.pack(fill="x", pady=(30, 0))

    def iniciar_sesion(self):
        usuario = self.user_entry.get()
        contrasena = self.pass_entry.get()

        auth = Autenticacion(
            gestor="sqlserver",
            host="localhost\\SQLEXPRESS",
            database="cubolap"
        )

        if auth.login(usuario, contrasena):
            messagebox.showinfo("Éxito", "Inicio de sesión correcto ✅")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos ❌")


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()