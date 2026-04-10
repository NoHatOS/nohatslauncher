import customtkinter as ctk
import os

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

    # Configuración de la ventana
        self.title("My Games")
        self.geometry("600x450")

        # Título superior
        self.label = ctk.CTkLabel(self, text="MIS JUEGOS", font=("Inter", 20, "bold"))
        self.label.pack(pady=20)

        # Botón de Engranaje (Configuración) arriba a la derecha
        self.settings_btn = ctk.CTkButton(self, text="⚙", width=30, fg_color="transparent", 
                                          hover_color="#333333", command=self.open_settings)
        self.settings_btn.place(relx=0.95, rely=0.05, anchor="ne")

        # Contenedor de juegos (Grid)
        self.games_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.games_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Ejemplo de un "Bloque" de juego
        self.add_game_block("Minecraft", "C:/Ruta/Al/Juego.exe")
        self.add_game_block("Valorant", "C:/Ruta/Al/Juego.exe")

    def add_game_block(self, name, path):
        # Crear un bloque (frame) para el juego
        game_card = ctk.CTkFrame(self.games_frame, width=150, height=150, corner_radius=10)
        game_card.pack(side="left", padx=10)

        title = ctk.CTkLabel(game_card, text=name, font=("Inter", 14))
        title.pack(pady=10)

        play_btn = ctk.CTkButton(game_card, text="JUGAR", width=100, height=32, 
                                 command=lambda: self.launch_game(path))
        play_btn.pack(pady=10)

    def launch_game(self, path):
        print(f"Abriendo: {path}")
        # os.startfile(path) # Esto abriría el juego en Windows

    def open_settings(self):
        print("Abriendo configuración...")

if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
