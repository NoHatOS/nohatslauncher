import customtkinter as ctk
from tkinter import filedialog
import json
import os

ctk.set_appearance_mode("dark")

# Tipografías elegantes
FONT_LIGHT = ("Segoe UI Light", 13)
FONT_SMALL = ("Segoe UI Semibold", 9)

class UltraLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.geometry("380x550")
        self.configure(fg_color="#000000")
        self.resizable(False, False)
        
        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_minimal_v6.json")
        self.juegos = self.cargar_datos()

        # --- PANEL DESPLEGABLE (INTERNO) ---
        self.menu_visible = False
        self.container_add = ctk.CTkFrame(self, fg_color="#050505", height=0, corner_radius=0, border_width=1, border_color="#111111")
        self.container_add.pack(fill="x", side="top")
        self.container_add.pack_propagate(False) # Evita que se ajuste al contenido antes de tiempo

        # Contenido dentro del menú desplegable
        self.entry_name = ctk.CTkEntry(self.container_add, placeholder_text="Nombre de la app", 
                                       fg_color="#000000", border_color="#222222", 
                                       height=28, font=FONT_LIGHT)
        self.entry_name.pack(pady=(15, 5), padx=50, fill="x")
        
        self.path_temp = ""
        self.btn_sel = ctk.CTkButton(self.container_add, text="Seleccionar archivo .exe", 
                                     fg_color="#111111", hover_color="#1A1A1A", 
                                     height=25, font=FONT_LIGHT, command=self.seleccionar_exe)
        self.btn_sel.pack(pady=5)

        self.btn_save = ctk.CTkButton(self.container_add, text="GUARDAR", fg_color="#FFFFFF", 
                                      text_color="#000000", height=25, width=100,
                                      font=FONT_SMALL, command=self.guardar_juego)
        self.btn_save.pack(pady=(5, 15))

        # --- BARRA SUPERIOR ---
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.header.pack(fill="x", padx=20, pady=5)

        self.btn_toggle = ctk.CTkButton(self.header, text="+", font=("Segoe UI Light", 28), 
                                        width=30, height=30, fg_color="transparent", 
                                        text_color="#FFFFFF", hover_color="#111111",
                                        command=self.toggle_menu)
        self.btn_toggle.pack(side="right")

        # --- CONTENEDOR DE APPS ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=5)
        self.scroll.columnconfigure((0, 1), weight=1)

        self.renderizar_apps()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f: return json.load(f)
        return []

    def toggle_menu(self):
        if not self.menu_visible:
            self.container_add.configure(height=160)
            self.btn_toggle.configure(text="×", text_color="#555555") 
        else:
            self.container_add.configure(height=0)
            self.btn_toggle.configure(text="+", text_color="#FFFFFF")
        self.menu_visible = not self.menu_visible

    def seleccionar_exe(self):
        p = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        if p:
            self.path_temp = p
            self.btn_sel.configure(text="Archivo listo", fg_color="#FFFFFF", text_color="#000000")

    def guardar_juego(self):
        if self.entry_name.get() and self.path_temp:
            self.juegos.append({"nombre": self.entry_name.get(), "ruta": self.path_temp})
            with open(self.db_file, "w") as f: json.dump(self.juegos, f)
            self.renderizar_apps()
            self.entry_name.delete(0, 'end')
            self.path_temp = ""
            self.btn_sel.configure(text="Seleccionar archivo .exe", fg_color="#111111", text_color="#FFFFFF")
            self.toggle_menu()

    def renderizar_apps(self):
        for w in self.scroll.winfo_children(): w.destroy()

        for i, app in enumerate(self.juegos):
            # Cajitas pequeñas (Barras compactas)
            card = ctk.CTkFrame(self.scroll, fg_color="#080808", corner_radius=4, 
                                border_width=1, border_color="#121212", height=38)
            card.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="nsew")
            card.pack_propagate(False)

            # Texto de la app
            lbl = ctk.CTkLabel(card, text=app["nombre"].lower(), font=FONT_LIGHT, text_color="#777777")
            lbl.pack(side="left", padx=10)

            # Botón run minimalista
            btn = ctk.CTkButton(card, text="run", width=35, height=18, fg_color="#111111",
                                hover_color="#FFFFFF", text_color="#FFFFFF", 
                                font=("Segoe UI", 8, "bold"), corner_radius=2)
            # Hover dinámico para el botón pequeño
            btn.configure(command=lambda r=app["ruta"]: os.startfile(r))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(text_color="#000000"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(text_color="#FFFFFF"))
            btn.pack(side="right", padx=8)

if __name__ == "__main__":
    app = UltraLauncher()
    app.mainloop()
