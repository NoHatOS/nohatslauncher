import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Estética Minimalista Extrema
BG_BLACK = "#050505"      # Negro casi absoluto
CARD_GRAY = "#111111"     # Gris muy sutil para bloques
TEXT_WHITE = "#E0E0E0"
ACCENT = "#1A1A1A"        # Gris oscuro para botones

class MiniLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana Pequeña y Centrada
        self.title("") 
        self.geometry("400x500") # Tamaño mini
        self.configure(fg_color=BG_BLACK)
        self.resizable(False, False)

        self.db_file = "games_data.json"
        self.juegos = self.cargar_datos()

        # --- CABECERA ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=15)

        self.title_label = ctk.CTkLabel(self.header, text="GAMES", 
                                        font=("Inter", 16, "bold"), text_color=TEXT_WHITE)
        self.title_label.pack(side="left")

        # Engranaje pequeño arriba a la derecha
        self.btn_cfg = ctk.CTkButton(self.header, text="⚙", width=25, height=25,
                                     fg_color="transparent", hover_color=CARD_GRAY,
                                     text_color="gray", command=self.abrir_config)
        self.btn_cfg.pack(side="right")

        # --- CONTENEDOR GRID (2 JUEGOS POR FILA) ---
        # Usamos un Frame con scroll por si tienes muchos juegos
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar las 2 columnas iguales
        self.main_container.grid_columnconfigure((0, 1), weight=1)

        self.dibujar_grid()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def guardar_datos(self):
        with open(self.db_file, "w") as f:
            json.dump(self.juegos, f)

    def dibujar_grid(self):
        # Limpiar
        for w in self.main_container.winfo_children():
            w.destroy()

        # Crear bloques en 2 columnas
        for i, juego in enumerate(self.juegos):
            fila = i // 2
            columna = i % 2
            
            card = ctk.CTkFrame(self.main_container, fg_color=CARD_GRAY, corner_radius=8, height=120)
            card.grid(row=fila, column=columna, padx=8, pady=8, sticky="nsew")
            card.pack_propagate(False)

            name_lbl = ctk.CTkLabel(card, text=juego["nombre"].lower(), 
                                    font=("Inter", 12), text_color=TEXT_WHITE)
            name_lbl.pack(pady=(20, 10))

            play_btn = ctk.CTkButton(card, text="play", width=80, height=24,
                                     fg_color=ACCENT, hover_color="#252525",
                                     font=("Inter", 11), corner_radius=4,
                                     command=lambda p=juego["ruta"]: os.startfile(p))
            play_btn.pack(pady=5)

    def abrir_config(self):
        # Ventana de configuración mini
        modal = ctk.CTkToplevel(self)
        modal.title("+")
        modal.geometry("300x200")
        modal.configure(fg_color=CARD_GRAY)
        modal.attributes("-topmost", True)
        modal.resizable(False, False)

        nombre_var = ctk.StringVar()
        ruta_var = ctk.StringVar()

        ctk.CTkEntry(modal, placeholder_text="Nombre del juego", textvariable=nombre_var,
                     fg_color=BG_BLACK, border_color=ACCENT).pack(pady=(20, 10), padx=20, fill="x")

        def buscar_exe():
            path = filedialog.askopenfilename(filetypes=[("Exe", "*.exe")])
            ruta_var.set(path)

        ctk.CTkButton(modal, text="Buscar .exe", fg_color=ACCENT, command=buscar_exe).pack(pady=5)

        def save():
            if nombre_var.get() and ruta_var.get():
                self.juegos.append({"nombre": nombre_var.get(), "ruta": ruta_var.get()})
                self.guardar_datos()
                self.dibujar_grid()
                modal.destroy()

        ctk.CTkButton(modal, text="Añadir", fg_color="white", text_color="black", command=save).pack(pady=20)

if __name__ == "__main__":
    app = MiniLauncher()
    app.mainloop()
