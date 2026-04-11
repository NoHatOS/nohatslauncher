import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Configuración de apariencia
ctk.set_appearance_mode("dark")

# Tipografías
FONT_LIGHT = ("Segoe UI Light", 13)
FONT_BOLD = ("Segoe UI Semibold", 10)

class LauncherSimple(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Launcher")
        self.geometry("380x600")
        self.configure(fg_color="#000000")
        self.resizable(False, False)
        
        # --- CARGAR ICONO .ICO ---
        # Busca el archivo "smile.ico" en la misma carpeta que el script
        try:
            self.iconbitmap("smile.ico")
        except:
            print("No se encontró smile.ico, usando icono por defecto")

        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_data.json")
        self.juegos = self.cargar_datos()

        # --- INTERFAZ ---
        self.menu_visible = False
        self.container_add = ctk.CTkFrame(self, fg_color="#080808", height=0, corner_radius=0, border_width=1, border_color="#1A1A1A")
        self.container_add.pack(fill="x", side="top")
        self.container_add.pack_propagate(False) 

        self.entry_name = ctk.CTkEntry(self.container_add, placeholder_text="Nombre de la App", fg_color="#000000", border_color="#222222", height=28, font=FONT_LIGHT)
        self.entry_name.pack(pady=(20, 5), padx=50, fill="x")
        
        self.path_temp = ""
        self.btn_sel = ctk.CTkButton(self.container_add, text="Seleccionar .exe", fg_color="#1A1A1A", height=25, font=FONT_LIGHT, command=self.seleccionar_exe)
        self.btn_sel.pack(pady=5)

        ctk.CTkButton(self.container_add, text="GUARDAR", fg_color="#FFFFFF", text_color="#000000", height=28, width=100, font=FONT_BOLD, corner_radius=14, command=self.guardar_juego).pack(pady=(5, 15))

        # Cabecera
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=45)
        self.header.pack(fill="x", padx=15, pady=(10, 0))

        self.btn_toggle = ctk.CTkButton(self.header, text="+", font=("Segoe UI Light", 26), width=35, height=35, fg_color="transparent", text_color="#FFFFFF", hover_color="#111111", command=self.toggle_menu)
        self.btn_toggle.pack(side="right")

        # Lista
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=0, pady=5)
        self.renderizar_apps()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f: return json.load(f)
            except: return []
        return []

    def toggle_menu(self):
        h = 170 if not self.menu_visible else 0
        self.container_add.configure(height=h)
        self.btn_toggle.configure(text="×" if not self.menu_visible else "+")
        self.menu_visible = not self.menu_visible

    def seleccionar_exe(self):
        p = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        if p:
            self.path_temp = p
            self.btn_sel.configure(text="Listo", fg_color="#FFFFFF", text_color="#000000")

    def guardar_juego(self):
        if self.entry_name.get() and self.path_temp:
            self.juegos.append({"nombre": self.entry_name.get(), "ruta": self.path_temp})
            self.salvar_y_refrescar()
            self.entry_name.delete(0, 'end')
            self.path_temp = ""
            self.btn_sel.configure(text="Seleccionar .exe", fg_color="#1A1A1A", text_color="#FFFFFF")
            self.toggle_menu()

    def eliminar_juego(self, indice):
        self.juegos.pop(indice)
        self.salvar_y_refrescar()

    def salvar_y_refrescar(self):
        with open(self.db_file, "w") as f: json.dump(self.juegos, f)
        self.renderizar_apps()

    def renderizar_apps(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for i, app in enumerate(self.juegos):
            linea = ctk.CTkFrame(self.scroll, fg_color="transparent", height=55)
            linea.pack(fill="x")
            linea.pack_propagate(False)

            ctk.CTkButton(linea, text="×", width=20, height=20, fg_color="transparent", text_color="#333333", hover_color="#330000", command=lambda idx=i: self.eliminar_juego(idx)).pack(side="left", padx=(20, 10))
            ctk.CTkLabel(linea, text=app["nombre"].lower(), font=FONT_LIGHT, text_color="#FFFFFF").pack(side="left")
            ctk.CTkButton(linea, text="RUN", width=55, height=24, fg_color="transparent", border_width=1, border_color="#FFFFFF", text_color="#FFFFFF", font=FONT_BOLD, corner_radius=4, command=lambda r=app["ruta"]: os.startfile(r)).pack(side="right", padx=25)
            
            ctk.CTkFrame(linea, fg_color="#111111", height=1).place(rely=1, relwidth=1, anchor="s")

if __name__ == "__main__":
    app = LauncherSimple()
    app.mainloop()
