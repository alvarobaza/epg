import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
# Mantenemos los IDs originales para buscarlos en la fuente
CANALES_ORIGINALES = ["iTVN", "iTVN extra"] 
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "guia_personalizada.xml"

def corregir_hora(timestr, horas):
    formato = "%Y%m%d%H%M%S %z"
    try:
        dt = datetime.strptime(timestr, formato)
        dt_corregida = dt + timedelta(hours=horas)
        return dt_corregida.strftime(formato)
    except:
        return timestr

def main():
    print("Descargando EPG original...")
    r = requests.get(URL_EPG)
    root = ET.fromstring(r.content)
    
    nuevo_root = ET.Element("tv")
    
    # 1. Procesar Canales
    for canal in root.findall("channel"):
        original_id = canal.get("id")
        if original_id in CANALES_ORIGINALES:
            # Cambiamos el ID del canal para el nuevo archivo
            nuevo_id = f"a@ {original_id}"
            canal.set("id", nuevo_id)
            
            # Cambiamos también el nombre visible (display-name)
            for name in canal.findall("display-name"):
                name.text = f"a@ {name.text}"
            
            nuevo_root.append(canal)
            
    # 2. Procesar Programas
    for programa in root.findall("programme"):
        original_channel = programa.get("channel")
        if original_channel in CANALES_ORIGINALES:
            # IMPORTANTE: El programa debe apuntar al nuevo ID "a@ ..."
            programa.set("channel", f"a@ {original_channel}")
            
            # Corregir las 6 horas
            programa.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            programa.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            
            nuevo_root.append(programa)
            
    # Guardar nuevo XML
    tree = ET.ElementTree(nuevo_root)
    tree.write(ARCHIVO_SALIDA, encoding="utf-8", xml_declaration=True)
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito con prefijos 'a@'.")

if __name__ == "__main__":
    main()
