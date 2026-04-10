import customtkinter as ctk
from tkinter import filedialog
import json
import os
import sys

# Forzar modo oscuro total
ctk.set_appearance_mode("dark")

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.geometry("380x500")
        self.configure(fg_color="#000000") 
        self.resizable(False, False)
        
        # SOLUCIÓN AL ERROR 13: Usamos un nombre de archivo único en la carpeta temporal de usuario
        # Esto evita cualquier bloqueo de permisos de la carpeta Downloads
        self.db_file = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "my_launcher_v3.json")
        
        self.juegos = self.cargar_datos()

        # --- CABECERA ---
        # "Library" - Blanco puro, negrita
        self.lbl_title = ctk.CTkLabel(self, text="Library", font=("Arial", 18, "bold"), text_color="#FFFFFF")
        self.lbl_title.place(x=20, y=20)

        # "Add" - Blanco puro, centrado en la esquina superior derecha
        self.btn_add = ctk.CTkButton(self, text="Add", width=60, height=28,
                                     fg_color="transparent", text_color="#FFFFFF",
                                     hover_color="#1A1A1A", font=("Arial", 14, "bold"),
                                     command=self.abrir_ajustes)
        self.btn_add.place(relx=0.95, rely=0.05, anchor="ne")

        # Contenedor de juegos
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

    def guardar_datos(self):
        # Intentar guardar y atrapar el error de permisos específicamente
        try:
            with open(self.db_file, "w") as f:
                json.dump(self.juegos, f)
            return True
        except PermissionError:
            # Si falla, intentamos guardar con otro nombre temporal
            self.db_file = self.db_file.replace(".json", "_backup.json")
            with open(self.db_file, "w") as f:
                json.dump(self.juegos, f)
            return True
        except Exception as e:
            print(f"Error fatal: {e}")
            return False

    def dibujar_juegos(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i, j in enumerate(self.juegos):
            card = ctk.CTkFrame(self.scroll, fg_color="#0A0A0A", border_width=1, border_color="#1A1A1A", height=145)
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=j["nombre"].capitalize(), font=("Arial", 13, "bold"), text_color="#FFFFFF").pack(pady=(25, 10))
            
            btn_play = ctk.CTkButton(card, text="PLAY", width=80, height=26, 
                                     fg_color="#FFFFFF", text_color="#000000",
                                     hover_color="#DDDDDD", font=("Arial", 11, "bold"),
                                     command=lambda r=j["ruta"]: self.lanzar(r))
            btn_play.pack(side="bottom", pady=20)

    def lanzar(self, ruta):
        try:
            os.startfile(ruta)
        except:
            pass

    def abrir_ajustes(self):
        top = ctk.CTkToplevel(self)
        top.title("Add")
        top.geometry("300x230")
        top.configure(fg_color="#0A0A0A")
        top.attributes("-topmost", True)
        top.grab_set()

        ctk.CTkLabel(top, text="Game Name", font=("Arial", 12, "bold"), text_color="#FFFFFF").pack(pady=(20, 5))
        name_in = ctk.CTkEntry(top, fg_color="#000000", border_color="#222222", text_color="#FFFFFF")
        name_in.pack(pady=5, padx=30, fill="x")

        path_ref = {"url": ""}

        def browse():
            p = filedialog.askopenfilename(filetypes=[("Exe", "*.exe")])
            if p: 
                path_ref["url"] = p
                btn_file.configure(text="Selected!", fg_color="#1A4A1A")

        btn_file = ctk.CTkButton(top, text="Select .exe", fg_color="#1A1A1A", text_color="#FFFFFF", command=browse)
        btn_file.pack(pady=15)

        def save_and_close():
            if name_in.get() and path_ref["url"]:
                self.juegos.append({"nombre": name_in.get(), "ruta": path_ref["url"]})
                if self.guardar_datos():
                    self.dibujar_juegos()
                    top.destroy()

        ctk.CTkButton(top, text="Save", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 12, "bold"), command=save_and_close).pack(pady=10)

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
