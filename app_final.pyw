import customtkinter as ctk
from tkinter import filedialog
import json
import os

ctk.set_appearance_mode("dark")

# Tipografías ULTRA-ELEGANTES (Seguimos el estilo "Light")
FONT_LIGHT = ("Segoe UI Light", 14)
FONT_BOLD = ("Segoe UI Semibold", 11)
FONT_MENU = ("Segoe UI Light", 13)

class ProLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- VENTANA COMPACTA ---
        self.title("")
        self.geometry("380x600")
        self.configure(fg_color="#000000") # NEGRO ABSOLUTO
        self.resizable(False, False)
        
        # Ruta de datos segura
        self.db_file = os.path.join(os.path.expanduser("~"), "launcher_elegant_v7.json")
        self.juegos = self.cargar_datos()

        # --- PANEL DESPLEGABLE (INTERNO) ---
        self.menu_visible = False
        self.container_add = ctk.CTkFrame(self, fg_color="#0A0A0A", height=0, corner_radius=0, border_width=1, border_color="#1A1A1A")
        self.container_add.pack(fill="x", side="top")
        self.container_add.pack_propagate(False) 

        # Contenido del menú desplegable (Estilo Fino)
        self.entry_name = ctk.CTkEntry(self.container_add, placeholder_text="Nombre de la app", 
                                       fg_color="#000000", border_color="#222222", 
                                       height=28, font=FONT_MENU, corner_radius=4)
        self.entry_name.pack(pady=(20, 5), padx=50, fill="x")
        
        self.path_temp = ""
        self.btn_sel = ctk.CTkButton(self.container_add, text="Seleccionar archivo .exe", 
                                     fg_color="#1A1A1A", hover_color="#252525", 
                                     height=25, font=FONT_MENU, corner_radius=4, command=self.seleccionar_exe)
        self.btn_sel.pack(pady=5)

        self.btn_save = ctk.CTkButton(self.container_add, text="GUARDAR", fg_color="#FFFFFF", 
                                      text_color="#000000", height=28, width=110,
                                      font=FONT_BOLD, corner_radius=14, command=self.guardar_juego)
        self.btn_save.pack(pady=(5, 15))

        # --- CABECERA ---
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=45)
        self.header.pack(fill="x", padx=25, pady=(10, 0))

        # El botón '+' más grande y elegante
        self.btn_toggle = ctk.CTkButton(self.header, text="+", font=("Segoe UI Light", 26), 
                                        width=35, height=35, fg_color="transparent", 
                                        text_color="#FFFFFF", hover_color="#111111",
                                        command=self.toggle_menu)
        self.btn_toggle.pack(side="right")

        # --- CONTENEDOR DE APPS (ESTILO LÍNEA COMPLETA) ---
        # He quitado los márgenes laterales del ScrollableFrame para que las líneas toquen el borde
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=0, pady=5)
        self.scroll.columnconfigure(0, weight=1)

        self.renderizar_apps()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f: return json.load(f)
            except: return []
        return []

    def toggle_menu(self):
        if not self.menu_visible:
            self.container_add.configure(height=170)
            self.btn_toggle.configure(text="×", text_color="#666666") 
        else:
            self.container_add.configure(height=0)
            self.btn_toggle.configure(text="+", text_color="#FFFFFF")
        self.menu_visible = not self.menu_visible

    def seleccionar_exe(self):
        p = filedialog.askopenfilename(filetypes=[("Executables", "*.exe")])
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
            self.btn_sel.configure(text="Seleccionar archivo .exe", fg_color="#1A1A1A", text_color="#FFFFFF")
            self.toggle_menu()

    def renderizar_apps(self):
        for w in self.scroll.winfo_children(): w.destroy()

        for i, app in enumerate(self.juegos):
            # Línea horizontal de ancho completo
            # El secreto es usar corner_radius=0 y border_width=0 en los lados
            card = ctk.CTkFrame(self.scroll, fg_color="transparent", corner_radius=0, height=55)
            # Solo añadimos un borde inferior muy sutil para separar líneas
            card.pack(fill="x", padx=0, pady=0)
            card.pack_propagate(False)

            # Nombre de la app (Blanco Puro y Elegante, a la izquierda)
            lbl = ctk.CTkLabel(card, text=app["nombre"].capitalize(), 
                               font=FONT_LIGHT, text_color="#FFFFFF")
            lbl.pack(side="left", padx=25)

            # Botón play ultra-minimal (solo texto grisaceo que se ilumina)
            btn = ctk.CTkButton(card, text="run", width=45, height=22, fg_color="transparent",
                                hover_color="#111111", text_color="#555555", 
                                font=("Segoe UI Semibold", 10), corner_radius=11)
            btn.configure(command=lambda r=app["ruta"]: self.lanzar_seguro(r))
            
            # Hover interactivo suave para el texto del botón
            btn.bind("<Enter>", lambda e, b=btn: b.configure(text_color="#FFFFFF"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(text_color="#555555"))
            
            btn.pack(side="right", padx=25)

            # Línea separatoria sutil (no llega hasta el borde para darle más estilo)
            separator = ctk.CTkFrame(card, fg_color="#1A1A1A", height=1, corner_radius=0)
            separator.place(rely=1, relwidth=0.9, relx=0.05, anchor="s")

    def lanzar_seguro(self, ruta):
        try:
            os.startfile(ruta)
        except:
            pass # Si falla, la app no se cierra

if __name__ == "__main__":
    app = ProLauncher()
    app.mainloop()
