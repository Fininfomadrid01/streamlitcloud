import os
import json
import sys
from decimal import Decimal

# Añadir el directorio del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'iv_smile_project/lambda'))

from scraper.meff_scraper import scrape_meff_data, prepare_for_dynamodb

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def main():
    """
    Función principal que simula la ejecución de la Lambda localmente
    """
    try:
        # Ejecutar scraping completo
        print("Iniciando scraping...")
        all_data = scrape_meff_data()
        print("Scraping completado. Preparando datos para DynamoDB...")
        items = prepare_for_dynamodb(all_data)
        
        # Imprimir los datos obtenidos
        print("\nDatos obtenidos:")
        for item in items:
            print(f"\nFecha: {item['fecha']}")
            print(f"Tipo: {item['tipo']}")
            datos = json.loads(item['datos'])
            print(f"Número de registros: {len(datos)}")
            if datos:
                print("Primer registro de ejemplo:")
                print(json.dumps(datos[0], indent=2, default=decimal_default))
        
        print("\nProceso completado exitosamente!")
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        raise

if __name__ == "__main__":
    main() 