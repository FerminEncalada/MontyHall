import random
from typing import List


class JuegoMontyHall:
    """
    Clase base que implementa la lógica común del problema de Monty Hall.
    
    Attributes:
        total_opciones (int): Número total de opciones en el juego
        opcion_ganadora (int): Opción que contiene el premio
        eleccion_usuario (int): Opción elegida por el usuario
        opciones_reveladas (List[int]): Opciones que han sido reveladas
    """
    
    def __init__(self, total_opciones: int):
        """
        Inicializa el juego con el número total de opciones.
        
        Args:
            total_opciones: Número total de opciones disponibles
        """
        self.total_opciones = total_opciones
        self.opcion_ganadora = random.randint(1, total_opciones)
        self.eleccion_usuario = None
        self.opciones_reveladas = []
        
    def seleccionar_opcion(self, opcion: int) -> bool:
        """
        Registra la selección inicial del usuario.
        
        Args:
            opcion: Número de la opción seleccionada
            
        Returns:
            True si la selección es válida, False en caso contrario
        """
        if 1 <= opcion <= self.total_opciones:
            self.eleccion_usuario = opcion
            return True
        return False
    
    def _obtener_opciones_perdedoras(self) -> List[int]:
        """
        Obtiene la lista de opciones que no son ganadoras.
        
        Returns:
            Lista de números de opciones perdedoras
        """
        return [i for i in range(1, self.total_opciones + 1) 
                if i != self.opcion_ganadora]
    
    def verificar_victoria(self) -> bool:
        """
        Verifica si el usuario ganó el juego.
        
        Returns:
            True si el usuario eligió la opción ganadora
        """
        return self.eleccion_usuario == self.opcion_ganadora
    
    def reiniciar(self):
        """Reinicia el juego con nuevos valores aleatorios."""
        self.opcion_ganadora = random.randint(1, self.total_opciones)
        self.eleccion_usuario = None
        self.opciones_reveladas = []
