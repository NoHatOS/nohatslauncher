import customtkinter as ctk
from tkinter import filedialog
import json
import os

# 1. Configuración de Tema (Fuerza el Negro)
ctk.set_appearance_mode("dark")

class LauncherPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana compacta y limpia
        self.title("")
        self.geometry("380x550")
        self.configure(fg_color="#000000") # NEGRO TOTAL
        self.resizable(False, False)
        
        # Ruta de datos segura para evitar errores de permisos
        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_v100.json")
        self.juegos = self.cargar_datos()

        # --- CABECERA ---
        # "Library" en blanco puro y negrita
        self.lbl_library = ctk.CTkLabel(self, text="Library", 
                                        font=("Arial", 22, "bold"), 
                                        text_color="#FFFFFF")
        self.lbl_library.place(x=25, y=25)

        # Botón "Add" en la esquina derecha, blanco y minimalista
        self.btn_add = ctk.CTkButton(self, text="Add", width=50, height=30,
                                     fg_color="transparent", 
                                     text_color="#FFFFFF",
                                     hover_color="#1A1A1A", 
                                     font=("Arial", 15, "bold"),
                                     command=self.abrir_ventana_add)
        self.btn_add.place(relx=0.93, rely=0.06, anchor="ne")

        # --- CONTENEDOR DE JUEGOS (GRID) ---
        self.canvas = ctk.CTkScrollableFrame(self, fg_color="transparent", width=340, height=420)
        self.canvas.place(x=10, y=85)
        self.canvas.columnconfigure((0, 1), weight=1)

        self.refrescar_lista()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def refrescar_lista(self):
        for child in self.canvas.winfo_children():
            child.destroy()

        for i, juego in enumerate(self.juegos):
            # Bloque de juego (Tarjeta)
            card = ctk.CTkFrame(self.canvas, fg_color="#0D0D0D", corner_radius=10, 
                                border_width=1, border_color="#1A1A1A", height=150)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            card.pack_propagate(False)

            # Nombre del juego centrado
            name = ctk.CTkLabel(card, text=juego["nombre"].upper(), 
                                font=("Arial", 12, "bold"), text_color="#FFFFFF")
            name.pack(pady=(30, 10))

            # Botón Play blanco
            btn_play = ctk.CTkButton(card, text="PLAY", width=80, height=28,
                                     fg_color="#FFFFFF", text_color="#000000",
                                     hover_color="#CCCCCC", font=("Arial", 11, "bold"),
                                     command=lambda r=juego["ruta"]: os.startfile(r))
            btn_play.pack(side="bottom", pady=20)

    def abrir_ventana_add(self):
        # Ventana flotante para añadir
        modal = ctk.CTkToplevel(self)
        modal.title("Add Game")
        modal.geometry("320x280")
        modal.configure(fg_color="#0D0D0D")
        modal.attributes("-topmost", True)
        modal.grab_set()

        ctk.CTkLabel(modal, text="GAME NAME", font=("Arial", 11, "bold"), text_color="#666666").pack(pady=(30, 5))
        entry_name = ctk.CTkEntry(modal, fg_color="#000000", border_color="#222222", text_color="#FFFFFF")
        entry_name.pack(pady=5, padx=30, fill="x")

        path_data = {"val": ""}

        def get_path():
            p = filedialog.askopenfilename(filetypes=[("Executables", "*.exe")])
            if p: 
                path_data["val"] = p
                btn_sel.configure(text="FILE READY", fg_color="#FFFFFF", text_color="#000000")

        btn_sel = ctk.CTkButton(modal, text="SELECT EXE", fg_color="#1A1A1A", text_color="#FFFFFF", command=get_path)
        btn_sel.pack(pady=20)

        def save():
            if entry_name.get() and path_data["val"]:
                self.juegos.append({"nombre": entry_name.get(), "ruta": path_data["val"]})
                with open(self.db_file, "w") as f:
                    json.dump(self.juegos, f)
                self.refrescar_lista()
                modal.destroy()

        ctk.CTkButton(modal, text="SAVE GAME", fg_color="#FFFFFF", text_color="#000000", 
                      font=("Arial", 12, "bold"), command=save).pack(pady=10)

if __name__ == "__main__":
    app = LauncherPro()
    app.mainloop()
