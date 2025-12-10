import tkinter as tk
from modelos.juego_puertas import JuegoPuertas
from utils.constantes import *


class VistaPuertas:
    """
    Clase que representa la interfaz visual del juego de las 3 puertas.
    """
    
    def __init__(self, ventana, callback_volver):
        """
        Inicializa la vista del juego de puertas.
        
        Args:
            ventana: Ventana principal de tkinter
            callback_volver: Función para volver al menú
        """
        self.ventana = ventana
        self.callback_volver = callback_volver
        self.juego = JuegoPuertas()
        self.fase = "seleccion"  # seleccion, revelada, final
        self.puerta_revelada = None
        self.canvas_puertas = {}
        
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
            text="🚪 JUEGO DE LAS 3 PUERTAS",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.titulo.pack(pady=20)
        
        # Mensaje
        self.mensaje = tk.Label(
            self.frame_principal,
            text="Elige una puerta. Detrás de una hay un AUTO 🚗\n"
                 "y detrás de las otras dos hay CABRAS 🐐",
            font=FUENTE_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        self.mensaje.pack(pady=10)
        
        # Frame para las puertas
        self.frame_puertas = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        self.frame_puertas.pack(pady=40)
        
        # Crear las 3 puertas
        for i in range(1, 4):
            self.crear_puerta(i)
        
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
        
    def crear_puerta(self, numero):
        """
        Crea una puerta visual en el canvas.
        
        Args:
            numero: Número de la puerta (1-3)
        """
        frame = tk.Frame(self.frame_puertas, bg=COLOR_FONDO)
        frame.pack(side=tk.LEFT, padx=20)
        
        # Canvas para la puerta
        canvas = tk.Canvas(
            frame,
            width=150,
            height=200,
            bg=COLOR_FONDO,
            highlightthickness=0
        )
        canvas.pack()
        
        # Dibujar puerta cerrada
        self.dibujar_puerta_cerrada(canvas, numero)
        
        # Etiqueta con número
        label = tk.Label(
            frame,
            text=f"Puerta {numero}",
            font=FUENTE_TEXTO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        label.pack(pady=5)
        
        # Bind para click
        canvas.bind("<Button-1>", lambda e, n=numero: self.click_puerta(n))
        canvas.bind("<Enter>", lambda e: canvas.configure(cursor="hand2"))
        
        self.canvas_puertas[numero] = canvas
        
    def dibujar_puerta_cerrada(self, canvas, numero):
        """Dibuja una puerta cerrada."""
        # Puerta
        canvas.create_rectangle(10, 10, 140, 190, 
                               fill=COLOR_PUERTA_CERRADA,
                               outline="black", width=3)
        # Marco
        canvas.create_rectangle(20, 20, 130, 180,
                               outline="gold", width=2)
        # Número
        canvas.create_text(75, 50, text=str(numero),
                          font=("Arial", 30, "bold"),
                          fill="gold")
        # Manija
        canvas.create_oval(120, 95, 130, 105, fill="gold")
        
    def dibujar_puerta_abierta(self, canvas, numero, contenido):
        """Dibuja una puerta abierta con su contenido."""
        canvas.delete("all")
        # Fondo abierto
        canvas.create_rectangle(10, 10, 140, 190,
                               fill=COLOR_PUERTA_ABIERTA,
                               outline="black", width=3)
        # Contenido
        if contenido == "AUTO":
            canvas.create_text(75, 100, text="🚗",
                             font=("Arial", 60))
        else:
            canvas.create_text(75, 100, text="🐐",
                             font=("Arial", 60))
                             
    def dibujar_puerta_seleccionada(self, canvas, numero):
        """Dibuja una puerta seleccionada (con borde dorado)."""
        canvas.delete("all")
        self.dibujar_puerta_cerrada(canvas, numero)
        canvas.create_rectangle(5, 5, 145, 195,
                               outline=COLOR_PUERTA_SELECCIONADA,
                               width=5)
        
    def click_puerta(self, numero):
        """
        Maneja el click en una puerta.
        
        Args:
            numero: Número de la puerta clickeada
        """
        if self.fase == "seleccion":
            self.seleccionar_puerta(numero)
        
    def seleccionar_puerta(self, numero):
        """Procesa la selección de una puerta."""
        self.juego.seleccionar_opcion(numero)
        self.dibujar_puerta_seleccionada(self.canvas_puertas[numero], numero)
        
        # Revelar una puerta
        self.puerta_revelada = self.juego.revelar_puerta()
        self.dibujar_puerta_abierta(
            self.canvas_puertas[self.puerta_revelada],
            self.puerta_revelada,
            "CABRA"
        )
        
        self.mensaje.config(
            text=f"Has elegido la puerta {numero}.\n"
                 f"El presentador abre la puerta {self.puerta_revelada} con una CABRA 🐐"
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
            text="Mantener mi elección",
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
            text="Cambiar de puerta",
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
            text=f"Mantienes tu elección: Puerta {self.juego.eleccion_usuario}"
        )
        self.revelar_resultado()
        
    def cambiar_eleccion(self):
        """Cambia la elección del usuario."""
        eleccion_anterior = self.juego.eleccion_usuario
        self.juego.cambiar_eleccion()
        
        # Actualizar visualización
        self.dibujar_puerta_cerrada(self.canvas_puertas[eleccion_anterior],
                                    eleccion_anterior)
        self.dibujar_puerta_seleccionada(
            self.canvas_puertas[self.juego.eleccion_usuario],
            self.juego.eleccion_usuario
        )
        
        self.mensaje.config(
            text=f"Cambiaste de la puerta {eleccion_anterior} "
                 f"a la puerta {self.juego.eleccion_usuario}"
        )
        self.revelar_resultado()
        
    def revelar_resultado(self):
        """Revela el contenido de todas las puertas."""
        self.fase = "final"
        
        # Revelar todas las puertas
        for i in range(1, 4):
            contenido = self.juego.obtener_contenido_puerta(i)
            self.dibujar_puerta_abierta(self.canvas_puertas[i], i, contenido)
            
            # Marcar la elección del usuario
            if i == self.juego.eleccion_usuario:
                canvas = self.canvas_puertas[i]
                canvas.create_rectangle(5, 5, 145, 195,
                                       outline=COLOR_PUERTA_SELECCIONADA,
                                       width=5)
        
        # Mostrar resultado
        if self.juego.verificar_victoria():
            resultado = "¡FELICIDADES! ¡GANASTE EL AUTO! 🚗🎉"
            color = COLOR_BOTON_SUCCESS
        else:
            resultado = "¡Oh no! Ganaste una CABRA 🐐"
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
