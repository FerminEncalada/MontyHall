import tkinter as tk
from tkinter import ttk
from modelos.juego_cartas import JuegoCartas
from utils.constantes import *


class VistaCartas:
    """
    Clase que representa la interfaz visual del juego de las 52 cartas.
    """
    
    def __init__(self, ventana, callback_volver):
        """
        Inicializa la vista del juego de cartas.
        
        Args:
            ventana: Ventana principal de tkinter
            callback_volver: Función para volver al menú
        """
        self.ventana = ventana
        self.callback_volver = callback_volver
        self.juego = JuegoCartas()
        self.fase = "seleccion"  # seleccion, reveladas, final
        self.carta_oculta = None
        self.canvas_cartas = {}
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea los elementos de la interfaz del juego."""
        self.ventana.configure(bg=COLOR_FONDO)
        
        # Frame principal
        self.frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.titulo = tk.Label(
            self.frame_principal,
            text="🃏 JUEGO DE LAS 52 CARTAS",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.titulo.pack(pady=20)
        
        # Mensaje
        self.mensaje = tk.Label(
            self.frame_principal,
            text="Elige una carta. Una de ellas es la GANADORA ⭐",
            font=FUENTE_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        self.mensaje.pack(pady=10)
        
        # Frame con scroll para las cartas
        self.crear_area_cartas()
        
        # Frame para botones
        self.frame_botones = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_botones.pack(pady=20)
        
        # Botón volver
        btn_volver = tk.Button(
            self.frame_principal,
            text="🏠 Volver al Menú",
            font=FUENTE_BOTON,
            bg=COLOR_ACENTO,
            fg=COLOR_TEXTO,
            cursor="hand2",
            command=self.callback_volver
        )
        btn_volver.pack(pady=10)
        
    def crear_area_cartas(self):
        """Crea el área con scroll para mostrar las cartas."""
        # Frame contenedor
        container = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        container.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas_scroll = tk.Canvas(container, bg=COLOR_FONDO, 
                                 highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(container, orient="vertical", 
                                 command=canvas_scroll.yview)
        
        self.frame_cartas = tk.Frame(canvas_scroll, bg=COLOR_FONDO)
        
        self.frame_cartas.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=self.frame_cartas, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear las 52 cartas en una cuadrícula
        for i in range(1, 53):
            fila = (i - 1) // 13
            columna = (i - 1) % 13
            self.crear_carta_pequena(i, fila, columna)
            
    def crear_carta_pequena(self, numero, fila, columna):
        """
        Crea una carta pequeña en la cuadrícula.
        
        Args:
            numero: Número de la carta (1-52)
            fila: Fila en la cuadrícula
            columna: Columna en la cuadrícula
        """
        frame = tk.Frame(self.frame_cartas, bg=COLOR_FONDO)
        frame.grid(row=fila, column=columna, padx=3, pady=3)
        
        canvas = tk.Canvas(
            frame,
            width=60,
            height=80,
            bg=COLOR_FONDO,
            highlightthickness=0
        )
        canvas.pack()
        
        # Dibujar carta boca abajo
        self.dibujar_carta_dorso(canvas, numero)
        
        # Etiqueta con posición
        label = tk.Label(
            frame,
            text=f"#{numero}",
            font=("Arial", 8),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        label.pack()
        
        # Bind para click
        canvas.bind("<Button-1>", lambda e, n=numero: self.click_carta(n))
        canvas.bind("<Enter>", lambda e: canvas.configure(cursor="hand2"))
        
        self.canvas_cartas[numero] = canvas
        
    def dibujar_carta_dorso(self, canvas, numero):
        """Dibuja una carta boca abajo."""
        canvas.delete("all")
        # Dorso de la carta
        canvas.create_rectangle(5, 5, 55, 75,
                               fill=COLOR_CARTA_DORSO,
                               outline="white", width=2)
        # Patrón decorativo
        canvas.create_text(30, 40, text="🂠",
                          font=("Arial", 30),
                          fill="white")
        
    def dibujar_carta_frente(self, canvas, numero):
        """Dibuja una carta boca arriba."""
        canvas.delete("all")
        carta_texto = self.juego.obtener_carta(numero)
        color = self.juego.obtener_color_carta(numero)
        color_texto = COLOR_CARTA_ROJA if color == "red" else COLOR_CARTA_NEGRA
        
        # Frente de la carta
        canvas.create_rectangle(5, 5, 55, 75,
                               fill=COLOR_CARTA_FRENTE,
                               outline="gray", width=2)
        # Valor de la carta
        canvas.create_text(30, 40, text=carta_texto,
                          font=("Arial", 16, "bold"),
                          fill=color_texto)
        
    def dibujar_carta_seleccionada(self, canvas, numero):
        """Dibuja una carta seleccionada con borde dorado."""
        self.dibujar_carta_dorso(canvas, numero)
        canvas.create_rectangle(2, 2, 58, 78,
                               outline=COLOR_PUERTA_SELECCIONADA,
                               width=3)
        
    def click_carta(self, numero):
        """
        Maneja el click en una carta.
        
        Args:
            numero: Número de la carta clickeada
        """
        if self.fase == "seleccion":
            self.seleccionar_carta(numero)
        
    def seleccionar_carta(self, numero):
        """Procesa la selección de una carta."""
        self.juego.seleccionar_opcion(numero)
        
        # Marcar la carta seleccionada
        self.dibujar_carta_seleccionada(self.canvas_cartas[numero], numero)
        
        self.mensaje.config(
            text=f"Has elegido la carta #{numero}. Revelando cartas..."
        )
        
        # Después de un momento, revelar las cartas
        self.ventana.after(1000, self.revelar_cartas)
        
    def revelar_cartas(self):
        """Revela 50 de las 51 cartas restantes."""
        cartas_reveladas, self.carta_oculta = self.juego.revelar_cartas()
        
        # Revelar las cartas
        for carta in cartas_reveladas:
            self.dibujar_carta_frente(self.canvas_cartas[carta], carta)
        
        self.mensaje.config(
            text=f"Se han revelado 50 cartas.\n"
                 f"Tu carta: #{self.juego.eleccion_usuario} | "
                 f"Otra carta oculta: #{self.carta_oculta}"
        )
        
        self.fase = "decision"
        self.mostrar_botones_decision()
        
    def mostrar_botones_decision(self):
        """Muestra los botones para mantener o cambiar."""
        # Limpiar botones anteriores
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        btn_mantener = tk.Button(
            self.frame_botones,
            text="Mantener mi carta",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON_SUCCESS,
            fg=COLOR_TEXTO,
            width=20,
            height=2,
            cursor="hand2",
            command=self.mantener_eleccion
        )
        btn_mantener.pack(side=tk.LEFT, padx=10)
        
        btn_cambiar = tk.Button(
            self.frame_botones,
            text="Cambiar de carta",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON_WARNING,
            fg=COLOR_TEXTO,
            width=20,
            height=2,
            cursor="hand2",
            command=self.cambiar_eleccion
        )
        btn_cambiar.pack(side=tk.LEFT, padx=10)
        
    def mantener_eleccion(self):
        """Mantiene la elección actual."""
        self.mensaje.config(
            text=f"Mantienes tu carta: #{self.juego.eleccion_usuario}"
        )
        self.revelar_resultado()
        
    def cambiar_eleccion(self):
        """Cambia la elección del usuario."""
        eleccion_anterior = self.juego.eleccion_usuario
        self.juego.cambiar_eleccion(self.carta_oculta)
        
        # Actualizar visualización
        self.dibujar_carta_dorso(self.canvas_cartas[eleccion_anterior], 
                                eleccion_anterior)
        self.dibujar_carta_seleccionada(self.canvas_cartas[self.carta_oculta],
                                       self.carta_oculta)
        
        self.mensaje.config(
            text=f"Cambiaste de la carta #{eleccion_anterior} "
                 f"a la carta #{self.carta_oculta}"
        )
        self.revelar_resultado()
        
    def revelar_resultado(self):
        """Revela el resultado final."""
        self.fase = "final"
        
        # Revelar las dos cartas finales
        self.dibujar_carta_frente(self.canvas_cartas[self.juego.eleccion_usuario],
                                 self.juego.eleccion_usuario)
        self.dibujar_carta_frente(self.canvas_cartas[self.carta_oculta],
                                 self.carta_oculta)
        
        # Marcar la carta ganadora
        canvas_ganadora = self.canvas_cartas[self.juego.opcion_ganadora]
        canvas_ganadora.create_text(30, 10, text="⭐",
                                   font=("Arial", 12))
        
        # Mostrar resultado
        carta_ganadora = self.juego.obtener_carta(self.juego.opcion_ganadora)
        
        if self.juego.verificar_victoria():
            resultado = f"¡FELICIDADES! ¡GANASTE! 🎉\n" \
                       f"Carta ganadora: {carta_ganadora} (#{self.juego.opcion_ganadora})"
            color = COLOR_BOTON_SUCCESS
        else:
            resultado = f"¡Casi! No era la carta ganadora.\n" \
                       f"Carta ganadora: {carta_ganadora} (#{self.juego.opcion_ganadora})"
            color = "#dc3545"
        
        self.mensaje.config(text=resultado, fg=color)
        
        # Mostrar botones finales
        for widget in self.frame_botones.winfo_children():
            widget.destroy()
        
        btn_nuevo = tk.Button(
            self.frame_botones,
            text="🔄 Jugar de nuevo",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON_PRIMARY,
            fg=COLOR_TEXTO,
            width=20,
            height=2,
            cursor="hand2",
            command=self.reiniciar_juego
        )
        btn_nuevo.pack(pady=10)
        
    def reiniciar_juego(self):
        """Reinicia el juego."""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        self.__init__(self.ventana, self.callback_volver)
