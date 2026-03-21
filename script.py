import requests
import xml.etree.ElementTree as ET

URL_EPG = "https://epg.ovh/plar.xml"
# Estos IDs son sagrados, deben ser iguales al original
CANALES_BUSCADOS = ["iTVN", "iTVN extra"] 
ARCHIVO_SALIDA = "alvaroguia.xml"

def main():
    # Bajamos el original con la codificación correcta
    response = requests.get(URL_EPG)
    response.encoding = 'utf-8'
    
    # Cargamos el XML completo en memoria
    root = ET.fromstring(response.text)
    
    # Creamos un nuevo contenedor vacío
    nuevo_xml = ET.Element("tv")
    # Copiamos los atributos (generador, etc.) del original si los tiene
    for key, value in root.attrib.items():
        nuevo_xml.set(key, value)

    # 1. Buscamos y pegamos los canales
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_BUSCADOS:
            nuevo_xml.append(canal)

    # 2. Buscamos y pegamos los programas
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_BUSCADOS:
            nuevo_xml.append(programa)
            
    # Guardamos el resultado
    tree = ET.ElementTree(nuevo_xml)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
