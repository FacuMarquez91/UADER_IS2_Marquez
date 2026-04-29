import json
from threading import Lock
class CalculadoraImpuesto:
    _instancia = None #Almacena la unica instancia de la clase
    _lock = Lock()  #Candado para sincronizacion en entornos multihilos
    
    def __new__(cls, *args, **kwargs): #controla la creacion de instancias
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None: 
                    cls._instancia = super().__new__(cls)
        return cls._instancia 
    
    def __init__(self, archivo_config: str = None): #Inicializa la configuracion una sola vez
        if not hasattr(self, "_inicializado"):
            self._config= {}
            if archivo_config:
                self._cargar_desde_archivo(archivo_config) 
            self._inicializado = True
    
    def _cargar_desde_archivo(self, archivo: str)-> None: #Carga la configuracion desde un archivo JSON
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                self._config= json.load(f)
        except FileNotFoundError:
            print(f"Archivo de configuracion no encontrado: {archivo}") 
            self._config= {} 
        except json.JSONDecodeError as e: 
            print(f"Error en formato Json: {e} , usando configuracion vacia") 
            self._config={} 
            
    def obtener(self,clave:str, default=None): #obtiene un valor de configuracion ; clave: nombde de la clave a buscar ; default: balor por defecto si la clave no existe
        return self._config.get(clave, default) 
    
    def establecer(self, clave:str, valor)-> None: #establece un valor en la configuracion; clave: nombbre de la clave; valor: valor a guardar
        self._config[clave]= valor
        
    def __str__(self)-> str: #retorna una representacion legible de la configuracion
        return (f"Configuracion actual {self._config}")
    
    def calcular(self, base_imponible: float)-> float: #calcula la suma de impuestos sobre una base imponible
        return base_imponible * (0.21 + 0.05 + 0.012) 
    
def main():#demostracion del Patron singleton
    calculo_impuestos= CalculadoraImpuesto() 
    calculo_impuestos2= CalculadoraImpuesto()
    
    print("¿Son la misma instancia?", calculo_impuestos is calculo_impuestos2) #verifica que sean la misma instancia
    
    print("se realiza calculo de impuestos sobre 150.75", calculo_impuestos.calcular(150.75), 
          "monto final:", 150.75 + calculo_impuestos.calcular(150.75)) 
    print("se realiza calculo de impuestos sobre 425.30", calculo_impuestos2.calcular(425.30),
          "monto final: ", 425.30 + calculo_impuestos2.calcular(425.30))

if __name__ =="__main__":
    main()
    
