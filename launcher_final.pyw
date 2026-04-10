import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Configuración de estilo global
ctk.set_appearance_mode("dark")
FONT_MODERNA = "Segoe UI Light"
FONT_BOLD = "Segoe UI"

class UltraLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de Ventana
        self.title("")
        self.geometry("380x500")
        self.configure(fg_color="#000000")
        self.resizable(False, False)
        
        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_minimal_v5.json")
        self.juegos = self.cargar_datos()

        # --- MENU DESPLEGABLE (OCULTO POR DEFECTO) ---
        self.menu_visible = False
        self.menu_add = ctk.CTkFrame(self, fg_color="#0A0A0A", height=0, corner_radius=0)
        self.menu_add.place(relx=0.5, rely=0, anchor="n", relwidth=1)

        # Contenido del menú desplegable
        self.entry_name = ctk.CTkEntry(self.menu_add, placeholder_text="Nombre", fg_color="#000000", 
                                       border_color="#1A1A1A", font=(FONT_MODERNA, 12))
        self.entry_name.pack(pady=(15, 5), padx=40, fill="x")
        
        self.path_temp = ""
        self.btn_sel = ctk.CTkButton(self.menu_add, text="Seleccionar Archivo", fg_color="#111111", 
                                     hover_color="#1A1A1A", font=(FONT_MODERNA, 11), command=self.seleccionar_exe)
        self.btn_sel.pack(pady=5)

        self.btn_save = ctk.CTkButton(self.menu_add, text="GUARDAR", fg_color="#FFFFFF", text_color="#000000", 
                                      font=(FONT_BOLD, 10, "bold"), command=self.guardar_juego, height=25)
        self.btn_save.pack(pady=(5, 15))

        # --- CABECERA ---
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.header.pack(fill="x", padx=20, pady=(10, 0))

        # Icono + para desplegar/ocultar menú
        self.btn_toggle = ctk.CTkButton(self.header, text="+", font=(FONT_MODERNA, 24), width=30, height=30,
                                        fg_color="transparent", text_color="#FFFFFF", hover_color="#111111",
                                        command=self.toggle_menu)
        self.btn_toggle.pack(side="right")

        # --- LISTA DE APPS (GRID COMPACTO) ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=340, height=400)
        self.scroll.pack(fill="both", expand=True, padx=15, pady=10)
        self.scroll.columnconfigure((0, 1), weight=1)

        self.renderizar_apps()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f: return json.load(f)
        return []

    def toggle_menu(self):
        if not self.menu_visible:
            self.menu_add.configure(height=160)
            self.btn_toggle.configure(text="×") # Cambia + por una X
        else:
            self.menu_add.configure(height=0)
            self.btn_toggle.configure(text="+")
        self.menu_visible = not self.menu_visible

    def seleccionar_exe(self):
        p = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        if p:
            self.path_temp = p
            self.btn_sel.configure(text="Listo", fg_color="#FFFFFF", text_color="#000000")

    def guardar_juego(self):
        if self.entry_name.get() and self.path_temp:
            self.juegos.append({"nombre": self.entry_name.get(), "ruta": self.path_temp})
            with open(self.db_file, "w") as f: json.dump(self.juegos, f)
            self.renderizar_apps()
            self.entry_name.delete(0, 'end')
            self.path_temp = ""
            self.btn_sel.configure(text="Seleccionar Archivo", fg_color="#111111", text_color="#FFFFFF")
            self.toggle_menu()

    def renderizar_apps(self):
        for w in self.scroll.winfo_children(): w.destroy()

        for i, app in enumerate(self.juegos):
            # Barra horizontal pequeña
            card = ctk.CTkFrame(self.scroll, fg_color="#0A0A0A", corner_radius=5, 
                                border_width=1, border_color="#151515", height=45)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            card.pack_propagate(False)

            # Nombre a la izquierda (en minúsculas para más estilo)
            lbl = ctk.CTkLabel(card, text=app["nombre"].lower(), font=(FONT_MODERNA, 12), text_color="#888888")
            lbl.pack(side="left", padx=12)

            # Botón play pequeño a la derecha
            btn = ctk.CTkButton(card, text="run", width=40, height=20, fg_color="transparent",
                                hover_color="#1A1A1A", text_color="#FFFFFF", font=(FONT_BOLD, 9, "bold"),
                                command=lambda r=app["ruta"]: os.startfile(r))
            btn.pack(side="right", padx=10)

if __name__ == "__main__":
    app = UltraLauncher()
    app.mainloop()
