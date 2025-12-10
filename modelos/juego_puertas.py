import random
from modelos.juego_base import JuegoMontyHall


class JuegoPuertas(JuegoMontyHall):
    """
    Implementación del problema clásico de Monty Hall con 3 puertas.
    """
    
    def __init__(self):
        """Inicializa el juego de las 3 puertas."""
        super().__init__(3)
        
    def revelar_puerta(self) -> int:
        """
        Revela una puerta con cabra que no fue seleccionada por el usuario.
        
        Returns:
            Número de la puerta revelada
        """
        opciones_perdedoras = self._obtener_opciones_perdedoras()
        opciones_a_revelar = [p for p in opciones_perdedoras 
                              if p != self.eleccion_usuario]
        
        puerta_revelada = random.choice(opciones_a_revelar)
        self.opciones_reveladas.append(puerta_revelada)
        return puerta_revelada
    
    def obtener_puerta_restante(self) -> int:
        """
        Obtiene el número de la puerta restante (no elegida ni revelada).
        
        Returns:
            Número de la puerta restante
        """
        for i in range(1, 4):
            if i != self.eleccion_usuario and i not in self.opciones_reveladas:
                return i
        return -1
    
    def cambiar_eleccion(self):
        """Cambia la elección del usuario a la puerta restante."""
        self.eleccion_usuario = self.obtener_puerta_restante()
    
    def obtener_contenido_puerta(self, puerta: int) -> str:
        """
        Obtiene el contenido de una puerta específica.
        
        Args:
            puerta: Número de la puerta
            
        Returns:
            "AUTO" si es la puerta ganadora, "CABRA" en caso contrario
        """
        return "AUTO" if puerta == self.opcion_ganadora else "CABRA"
