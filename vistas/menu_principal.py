import tkinter as tk
from utils.constantes import *


class MenuPrincipal:
    """
    Clase que representa el menú principal de la aplicación.
    """
    
    def __init__(self, ventana):
        """
        Inicializa el menú principal.
        
        Args:
            ventana: Ventana principal de tkinter
        """
        self.ventana = ventana
        self.ventana.title("Paradoja de Monty Hall")
        self.ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.ventana.configure(bg=COLOR_FONDO)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea los elementos de la interfaz del menú."""
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = tk.Label(
            frame_principal,
            text="🎲 PARADOJA DE MONTY HALL",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        titulo.pack(pady=30)
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_principal,
            text="Elige tu modo de juego",
            font=FUENTE_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        subtitulo.pack(pady=10)
        
        # Frame para botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(pady=40)
        
        # Botón juego de puertas
        btn_puertas = tk.Button(
            frame_botones,
            text="🚪 JUEGO DE 3 PUERTAS\n\nJuego clásico",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON_PRIMARY,
            fg=COLOR_TEXTO,
            width=25,
            height=6,
            cursor="hand2",
            command=self.iniciar_juego_puertas
        )
        btn_puertas.pack(side=tk.LEFT, padx=20)
        
        # Botón juego de cartas
        btn_cartas = tk.Button(
            frame_botones,
            text="🃏 JUEGO DE 52 CARTAS\n\nVersión avanzada",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON_PRIMARY,
            fg=COLOR_TEXTO,
            width=25,
            height=6,
            cursor="hand2",
            command=self.iniciar_juego_cartas
        )
        btn_cartas.pack(side=tk.LEFT, padx=20)
        
        # Información
        info_frame = tk.Frame(frame_principal, bg=COLOR_FONDO_SECUNDARIO, 
                             relief=tk.RAISED, borderwidth=2)
        info_frame.pack(pady=30, padx=50, fill=tk.BOTH)
        
        info_titulo = tk.Label(
            info_frame,
            text="📚 ¿Qué es la Paradoja de Monty Hall?",
            font=("Arial", 14, "bold"),
            bg=COLOR_FONDO_SECUNDARIO,
            fg=COLOR_TEXTO
        )
        info_titulo.pack(pady=10)
        
        info_texto = tk.Label(
            info_frame,
            text="Es un problema de probabilidad contraintuitivo.\n"
                 "Cambiar tu elección inicial aumenta tus posibilidades de ganar.\n"
                 "• En 3 puertas: 66% de probabilidad al cambiar\n"
                 "• En 52 cartas: 98% de probabilidad al cambiar",
            font=FUENTE_TEXTO,
            bg=COLOR_FONDO_SECUNDARIO,
            fg=COLOR_TEXTO_SECUNDARIO,
            justify=tk.LEFT
        )
        info_texto.pack(pady=10, padx=20)
        
    def iniciar_juego_puertas(self):
        """Inicia el juego de las 3 puertas."""
        from vistas.vista_puertas import VistaPuertas
        self.limpiar_ventana()
        VistaPuertas(self.ventana, self.volver_menu)
        
    def iniciar_juego_cartas(self):
        """Inicia el juego de las 52 cartas."""
        from vistas.vista_cartas import VistaCartas
        self.limpiar_ventana()
        VistaCartas(self.ventana, self.volver_menu)
        
    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana."""
        for widget in self.ventana.winfo_children():
            widget.destroy()
            
    def volver_menu(self):
        """Vuelve al menú principal."""
        self.limpiar_ventana()
        self.__init__(self.ventana)
