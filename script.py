import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] 
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "alvaroguia.xml"

def corregir_hora(timestr, horas):
    # Formato original: 20260321200000 +0100
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
    r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    
    nuevo_root = ET.Element("tv")
    
    # 1. Copiamos los canales EXACTAMENTE como son originalmente
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_INTERES:
            nuevo_root.append(canal)
            
    # 2. Copiamos los programas con el ID original pero con la HORA CAMBIADA
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_INTERES:
            # Modificamos la hora en el mismo elemento
            programa.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            programa.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            nuevo_root.append(programa)
            
    # Guardar XML con declaración estándar
    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito.")

if __name__ == "__main__":
    main()
