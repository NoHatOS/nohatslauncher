import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Forzar modo oscuro total y tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MiniLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana compacta, limpia y SIN barra de título por defecto
        # (Usaremos la barra estándar para facilitar el cierre, pero muy minimal)
        self.title("")
        self.geometry("360x550")
        self.configure(fg_color="#000000") # NEGRO ABSOLUTO
        self.resizable(False, False)
        
        # Ruta de datos segura
        self.db_file = os.path.join(os.path.expanduser("~"), "my_launcher_v11.json")
        self.juegos = self.cargar_datos()

        # --- CABECERA (Solo Icono Add) ---
        # Creamos un frame para el icono "Add" gráfico
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", width=360, height=60)
        self.header_frame.place(x=0, y=10)
        self.header_frame.pack_propagate(False)

        # ICONO GRÁFICO "ADD" (Un '+' minimalista)
        # Usamos un CTkButton pero estilizado como icono
        self.btn_add_icon = ctk.CTkButton(self.header_frame, 
                                          text="+", # Símbolo simple
                                          font=("Arial", 26), 
                                          width=40, height=40,
                                          corner_radius=20, # Redondeado total
                                          fg_color="#111111", # Casi negro
                                          text_color="#FFFFFF",
                                          hover_color="#333333", # Gris oscuro al pasar el raton
                                          border_width=1,
                                          border_color="#222222",
                                          command=self.abrir_ventana_add)
        self.btn_add_icon.place(relx=0.92, rely=0.5, anchor="ne")

        # --- CONTENEDOR DE JUEGOS (GRID) ---
        self.canvas = ctk.CTkScrollableFrame(self, fg_color="transparent", width=330, height=440)
        self.canvas.place(x=15, y=80)
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
            # Bloque de juego (Tarjeta Minimal)
            card = ctk.CTkFrame(self.canvas, fg_color="#080808", corner_radius=12, 
                                border_width=1, border_color="#1A1A1A", height=160)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            card.pack_propagate(False)

            # Nombre del juego (Mayúsculas, fino)
            name = ctk.CTkLabel(card, text=juego["nombre"].upper(), 
                                font=("Inter Light", 11), text_color="#AAAAAA")
            name.pack(pady=(35, 10))

            # Botón Play blanco minimalista
            btn_play = ctk.CTkButton(card, text="PLAY", width=90, height=30,
                                     fg_color="#FFFFFF", text_color="#000000",
                                     hover_color="#DDDDDD", font=("Inter Bold", 12),
                                     corner_radius=15, # Muy redondeado
                                     command=lambda r=juego["ruta"]: os.startfile(r))
            btn_play.pack(side="bottom", pady=25)

    def abrir_ventana_add(self):
        # Ventana flotante estéticamente igual
        modal = ctk.CTkToplevel(self)
        modal.title("Add New")
        modal.geometry("320x280")
        modal.configure(fg_color="#080808")
        modal.attributes("-topmost", True)
        modal.grab_set()

        ctk.CTkLabel(modal, text="NEW GAME", font=("Inter Bold", 12), text_color="#FFFFFF").pack(pady=(35, 5))
        entry_name = ctk.CTkEntry(modal, fg_color="#000000", border_color="#222222", 
                                  text_color="#FFFFFF", corner_radius=8)
        entry_name.pack(pady=5, padx=30, fill="x")

        path_data = {"val": ""}

        def get_path():
            p = filedialog.askopenfilename(filetypes=[("Executables", "*.exe")])
            if p: 
                path_data["val"] = p
                btn_sel.configure(text="READY", fg_color="#FFFFFF", text_color="#000000")

        btn_sel = ctk.CTkButton(modal, text="SELECT EXE", fg_color="#1A1A1A", text_color="#FFFFFF",
                                 corner_radius=8, command=get_path)
        btn_sel.pack(pady=20)

        def save():
            if entry_name.get() and path_data["val"]:
                self.juegos.append({"nombre": entry_name.get(), "ruta": path_data["val"]})
                with open(self.db_file, "w") as f:
                    json.dump(self.juegos, f)
                self.refrescar_lista()
                modal.destroy()

        ctk.CTkButton(modal, text="SAVE", fg_color="#FFFFFF", text_color="#000000", 
                      font=("Inter Bold", 13), corner_radius=15, command=save).pack(pady=10)

if __name__ == "__main__":
    app = MiniLauncher()
    app.mainloop()
