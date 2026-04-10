import customtkinter as ctk
from tkinter import filedialog
import json
import os

ctk.set_appearance_mode("dark")

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.geometry("380x500")
        self.configure(fg_color="#000000") 
        
        # Guardamos en una ruta segura para evitar el error de permisos
        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_games_data.json")
        self.juegos = self.cargar_datos()

        # --- CABECERA ---
        # "Library" en blanco y con primera mayúscula
        self.lbl_title = ctk.CTkLabel(self, text="Library", font=("Arial", 16, "bold"), text_color="#FFFFFF")
        self.lbl_title.place(x=20, y=20)

        # "Add" más blanco y centrado en la esquina derecha
        self.btn_settings = ctk.CTkButton(self, text="Add", width=50, height=25,
                                          fg_color="transparent", text_color="#EEEEEE",
                                          hover_color="#111111", font=("Arial", 12, "bold"),
                                          command=self.abrir_ajustes)
        self.btn_settings.place(relx=0.95, rely=0.05, anchor="ne")

        # Contenedor
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=340, height=380)
        self.scroll.place(x=10, y=70)
        self.scroll.columnconfigure((0, 1), weight=1)

        self.dibujar_juegos()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    return json.load(f)
            except: return []
        return []

    def dibujar_juegos(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i, j in enumerate(self.juegos):
            card = ctk.CTkFrame(self.scroll, fg_color="#080808", border_width=1, border_color="#1A1A1A", height=140)
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=j["nombre"].capitalize(), font=("Arial", 12, "bold"), text_color="#FFFFFF").pack(pady=(20, 10))
            
            btn_play = ctk.CTkButton(card, text="PLAY", width=80, height=24, 
                                     fg_color="#FFFFFF", text_color="#000000",
                                     hover_color="#CCCCCC", font=("Arial", 10, "bold"),
                                     command=lambda r=j["ruta"]: self.lanzar(r))
            btn_play.pack(side="bottom", pady=20)

    def lanzar(self, ruta):
        try:
            os.startfile(ruta)
        except:
            print("No se pudo abrir el archivo")

    def abrir_ajustes(self):
        top = ctk.CTkToplevel(self)
        top.title("Add New Game")
        top.geometry("320x250")
        top.configure(fg_color="#080808")
        top.attributes("-topmost", True)
        top.grab_set()

        ctk.CTkLabel(top, text="Game Name", text_color="#FFFFFF").pack(pady=(20, 0))
        name_in = ctk.CTkEntry(top, fg_color="#000000", border_color="#333333")
        name_in.pack(pady=10, padx=30, fill="x")

        path_ref = {"url": ""}

        def browse():
            p = filedialog.askopenfilename(filetypes=[("Exe", "*.exe")])
            if p: path_ref["url"] = p

        ctk.CTkButton(top, text="Select Executable", fg_color="#1A1A1A", command=browse).pack(pady=5)

        def save():
            if name_in.get() and path_ref["url"]:
                self.juegos.append({"nombre": name_in.get(), "ruta": path_ref["url"]})
                # Intento de guardado con manejo de errores
                try:
                    with open(self.db_file, "w") as f:
                        json.dump(self.juegos, f)
                    self.dibujar_juegos()
                    top.destroy()
                except PermissionError:
                    print("Error: Cierra el archivo data.json si lo tienes abierto.")

        ctk.CTkButton(top, text="Save", fg_color="#FFFFFF", text_color="#000000", command=save).pack(pady=20)

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
