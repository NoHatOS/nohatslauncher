import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Forzar el tema oscuro antes de crear la app
ctk.set_appearance_mode("dark")

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana Mini y Compacta
        self.title("")
        self.geometry("350x500")
        self.configure(fg_color="#000000") # Negro absoluto
        
        self.db_file = "data.json"
        self.juegos = self.cargar_datos()

        # Título Minimal (Arriba a la izquierda)
        self.lbl_title = ctk.CTkLabel(self, text="library", font=("Arial", 16), text_color="#444444")
        self.lbl_title.place(x=25, y=20)

        # BOTÓN ENGRANAJE (Texto simple como pediste)
        self.btn_settings = ctk.CTkButton(self, text="edit", width=40, height=20,
                                          fg_color="transparent", text_color="#666666",
                                          hover_color="#111111", font=("Arial", 12),
                                          command=self.abrir_ajustes)
        self.btn_settings.place(relx=0.9, rely=0.05, anchor="ne")

        # Contenedor de juegos (Grid de 2 columnas)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=310, height=380)
        self.scroll.place(x=10, y=60)
        self.scroll.columnconfigure((0, 1), weight=1)

        self.dibujar_juegos()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def dibujar_juegos(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i, j in enumerate(self.juegos):
            # Bloque tipo "tarjeta"
            card = ctk.CTkFrame(self.scroll, fg_color="#080808", border_width=1, border_color="#151515", height=130)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=j["nombre"].lower(), font=("Arial", 11), text_color="#BBBBBB").pack(pady=(20, 10))
            
            btn_play = ctk.CTkButton(card, text="play", width=60, height=20, 
                                     fg_color="#FFFFFF", text_color="#000000",
                                     hover_color="#AAAAAA", font=("Arial", 10, "bold"),
                                     command=lambda r=j["ruta"]: os.startfile(r))
            btn_play.pack(side="bottom", pady=15)

    def abrir_ajustes(self):
        # Crear ventana de ajustes
        top = ctk.CTkToplevel(self)
        top.title("add")
        top.geometry("300x200")
        top.configure(fg_color="#050505")
        top.attributes("-topmost", True) # IMPORTANTE: Esto la pone al frente
        top.grab_set() # Bloquea la ventana principal hasta cerrar esta

        name_in = ctk.CTkEntry(top, placeholder_text="game name", fg_color="#000000", border_color="#222222")
        name_in.pack(pady=(30, 10), padx=20, fill="x")

        path_ref = {"url": ""}

        def browse():
            p = filedialog.askopenfilename(filetypes=[("Exe", "*.exe")])
            if p: path_ref["url"] = p

        ctk.CTkButton(top, text="select file", fg_color="#111111", command=browse).pack(pady=5)

        def save():
            if name_in.get() and path_ref["url"]:
                self.juegos.append({"nombre": name_in.get(), "ruta": path_ref["url"]})
                with open(self.db_file, "w") as f:
                    json.dump(self.juegos, f)
                self.dibujar_juegos()
                top.destroy()

        ctk.CTkButton(top, text="save", fg_color="#FFFFFF", text_color="#000000", command=save).pack(pady=15)

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
