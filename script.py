import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_ORIGINALES = ["iTVN", "iTVN extra"] 
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "alvaroguia.xml"
PREFIJO = "1a_"

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
            nuevo_id = f"{PREFIJO}{original_id}"
            canal.set("id", nuevo_id)
            for name in canal.findall("display-name"):
                name.text = f"{PREFIJO}{name.text}"
            nuevo_root.append(canal)
            
    # 2. Procesar Programas
    for programa in root.findall("programme"):
        original_channel = programa.get("channel")
        if original_channel in CANALES_ORIGINALES:
            programa.set("channel", f"{PREFIJO}{original_channel}")
            programa.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            programa.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            nuevo_root.append(programa)
            
    # Guardar nuevo XML
    tree = ET.ElementTree(nuevo_root)
    tree.write(ARCHIVO_SALIDA, encoding="utf-8", xml_declaration=True)
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito.")

if __name__ == "__main__":
    main()
