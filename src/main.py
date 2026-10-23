import sys
import os

RUTA_RAIZ = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.join(RUTA_RAIZ, "src")

if RUTA_SRC not in sys.path:
    sys.path.insert(0, RUTA_SRC)

from interfaz.motor_2d import Juego2D

def main():
    print("=" * 65)
    print("      H Y S T E R I A :   T H E   O T H E R   S I D E")
    print("      Iniciando Entorno Gráfico y Autómatas Formales")
    print("=" * 65)
    
    try:
        app = Juego2D()
        app.ejecutar()
    except Exception as e:
        print(f"\n[ERROR AL INICIAR EL JUEGO]: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()