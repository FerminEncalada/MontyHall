import random
from typing import List, Tuple
from modelos.juego_base import JuegoMontyHall


class JuegoCartas(JuegoMontyHall):
    """
    Implementación del problema de Monty Hall con 52 cartas.
    """
    
    PALOS = ['♠', '♥', '♦', '♣']
    VALORES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self):
        """Inicializa el juego de las 52 cartas."""
        super().__init__(52)
        self.baraja = self._crear_baraja()
        
    def _crear_baraja(self) -> List[str]:
        """
        Crea una baraja completa de 52 cartas.
        
        Returns:
            Lista de strings representando las cartas
        """
        baraja = []
        for palo in self.PALOS:
            for valor in self.VALORES:
                baraja.append(f"{valor}{palo}")
        return baraja
    
    def obtener_carta(self, posicion: int) -> str:
        """
        Obtiene la carta en una posición específica.
        
        Args:
            posicion: Posición de la carta (1-52)
            
        Returns:
            String representando la carta
        """
        return self.baraja[posicion - 1]
    
    def obtener_color_carta(self, posicion: int) -> str:
        """
        Obtiene el color de una carta (rojo o negro).
        
        Args:
            posicion: Posición de la carta (1-52)
            
        Returns:
            "red" o "black"
        """
        carta = self.obtener_carta(posicion)
        return "red" if '♥' in carta or '♦' in carta else "black"
    
    def revelar_cartas(self) -> Tuple[List[int], int]:
        """
        Revela 50 de las 51 cartas restantes, dejando oculta la carta ganadora
        (o una carta aleatoria si el usuario ya eligió la ganadora).
        
        Returns:
            Tupla con (lista de posiciones reveladas, posición de carta oculta)
        """
        cartas_no_elegidas = [i for i in range(1, 53) 
                             if i != self.eleccion_usuario]
        
        if self.eleccion_usuario == self.opcion_ganadora:
            carta_oculta = random.choice(cartas_no_elegidas)
        else:
            carta_oculta = self.opcion_ganadora
        
        cartas_reveladas = [i for i in cartas_no_elegidas if i != carta_oculta]
        self.opciones_reveladas = cartas_reveladas
        
        return cartas_reveladas, carta_oculta
    
    def cambiar_eleccion(self, nueva_carta: int):
        """
        Cambia la elección del usuario a otra carta.
        
        Args:
            nueva_carta: Posición de la nueva carta elegida
        """
        self.eleccion_usuario = nueva_carta
