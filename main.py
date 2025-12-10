import tkinter as tk
from vistas.menu_principal import MenuPrincipal


def main():
    """
    Función principal que inicia la aplicación.
    """
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Paradoja de Monty Hall")
    ventana.resizable(False, False)
    
    # Centrar ventana en la pantalla
    ventana.update_idletasks()
    ancho_ventana = 1200
    alto_ventana = 700
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')
    
    # Iniciar menú principal
    MenuPrincipal(ventana)
    
    # Iniciar loop de la aplicación
    ventana.mainloop()


if __name__ == "__main__":
    main()
