import customtkinter as ctk
from tkinter import filedialog
import json
import os

# Configuración visual: Negro profundo
COLOR_FONDO = "#0A0A0A"  # Negro casi puro
COLOR_TARJETA = "#161616" # Gris muy oscuro para los bloques
COLOR_ACCENTO = "#333333" # Para botones y hover
FONT_PRINCIPAL = "Segoe UI" # Fuente limpia y moderna

class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Game Station")
        self.geometry("700x500")
        self.configure(fg_color=COLOR_FONDO)

        # Archivo donde guardaremos tus juegos
        self.db_file = "mis_juegos.json"
        self.juegos = self.cargar_datos()

        # --- UI SUPERIOR ---
        self.label = ctk.CTkLabel(self, text="LIBRARY", 
                                  font=(FONT_PRINCIPAL, 24, "bold"), 
                                  text_color="#FFFFFF")
        self.label.pack(pady=(30, 10))

        # Botón Engranaje (Minimalista)
        self.settings_btn = ctk.CTkButton(self, text="⚙", width=40, height=40,
                                          fg_color="transparent",
                                          hover_color=COLOR_ACCENTO,
                                          text_color="gray",
                                          font=("Arial", 20),
                                          command=self.abrir_configuracion)
        self.settings_btn.place(relx=0.96, rely=0.04, anchor="ne")

        # --- CONTENEDOR DE JUEGOS ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", orientation="horizontal", height=250)
        self.scroll_frame.pack(fill="x", padx=20, pady=20)

        self.renderizar_juegos()

    def cargar_datos(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return []

    def guardar_datos(self):
        with open(self.db_file, "w") as f:
            json.dump(self.juegos, f)

    def renderizar_juegos(self):
        # Limpiar bloques actuales
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Crear bloques por cada juego guardado
        for juego in self.juegos:
            card = ctk.CTkFrame(self.scroll_frame, width=180, height=200, 
                                fg_color=COLOR_TARJETA, corner_radius=12)
            card.pack(side="left", padx=15, pady=10)
            card.pack_propagate(False)

            lbl = ctk.CTkLabel(card, text=juego["nombre"].upper(), 
                               font=(FONT_PRINCIPAL, 13, "bold"), text_color="#E0E0E0")
            lbl.pack(pady=(40, 20))

            btn = ctk.CTkButton(card, text="LAUNCH", 
                                fg_color=COLOR_ACCENTO,
                                hover_color="#444444",
                                corner_radius=20,
                                font=(FONT_PRINCIPAL, 11, "bold"),
                                command=lambda p=juego["ruta"]: self.ejecutar_juego(p))
            btn.pack(side="bottom", pady=20)

    def ejecutar_juego(self, ruta):
        try:
            os.startfile(ruta)
        except Exception as e:
            print(f"Error al abrir: {e}")

    def abrir_configuracion(self):
        # Ventana emergente para añadir juego
        ventana_add = ctk.CTkToplevel(self)
        ventana_add.title("Añadir Juego")
        ventana_add.geometry("400x300")
        ventana_add.configure(fg_color=COLOR_TARJETA)
        ventana_add.attributes("-topmost", True) # Que aparezca encima

        ctk.CTkLabel(ventana_add, text="NOMBRE DEL JUEGO", font=(FONT_PRINCIPAL, 12)).pack(pady=(20, 5))
        entrada_nombre = ctk.CTkEntry(ventana_add, width=250, fg_color=COLOR_FONDO, border_color=COLOR_ACCENTO)
        entrada_nombre.pack(pady=5)

        ruta_seleccionada = [""]

        def seleccionar_archivo():
            ruta = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
            if ruta:
                ruta_seleccionada[0] = ruta
                btn_file.configure(text="¡ARCHIVO LISTO!", fg_color="#225522")

        btn_file = ctk.CTkButton(ventana_add, text="SELECCIONAR .EXE", command=seleccionar_archivo, fg_color=COLOR_ACCENTO)
        btn_file.pack(pady=20)

        def confirmar():
            if entrada_nombre.get() and ruta_seleccionada[0]:
                self.juegos.append({"nombre": entrada_nombre.get(), "ruta": ruta_seleccionada[0]})
                self.guardar_datos()
                self.renderizar_juegos()
                ventana_add.destroy()

        ctk.CTkButton(ventana_add, text="GUARDAR", fg_color="#FFFFFF", text_color="black", command=confirmar).pack(pady=10)

if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
