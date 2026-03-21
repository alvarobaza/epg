import requests
import xml.etree.ElementTree as ET

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] 
ARCHIVO_SALIDA = "alvaroguia.xml"

def main():
    r = requests.get(URL_EPG)
    r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    
    nuevo_root = ET.Element("tv")

    # 1. Canales
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_INTERES:
            nuevo_root.append(canal)

    # 2. Programas
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_INTERES:
            nuevo_root.append(programa)
            
    # Guardar con la CABECERA COMPLETA que exige Android
    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b'<!DOCTYPE tv SYSTEM "xmltv.dtd">\n') # ESTA LÍNEA ES CLAVE
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
