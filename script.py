import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] # IDs exactos del XML original
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "guia_personalizada.xml"

def corregir_hora(timestr, horas):
    # Formato: 20260321200000 +0100
    formato = "%Y%m%d%H%M%S %z"
    dt = datetime.strptime(timestr, formato)
    dt_corregida = dt + timedelta(hours=horas)
    return dt_corregida.strftime(formato)

def main():
    print("Descargando EPG original...")
    r = requests.get(URL_EPG)
    root = ET.fromstring(r.content)
    
    nuevo_root = ET.Element("tv")
    
    # Filtrar canales
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_INTERES:
            nuevo_root.append(canal)
            
    # Filtrar programas y corregir hora
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_INTERES:
            # Corregir inicio y fin
            programa.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            programa.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            nuevo_root.append(programa)
            
    # Guardar nuevo XML
    tree = ET.ElementTree(nuevo_root)
    tree.write(ARCHIVO_SALIDA, encoding="utf-8", xml_declaration=True)
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito.")

if __name__ == "__main__":
    main()
