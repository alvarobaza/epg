import requests
import xml.etree.ElementTree as ET

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] 
ARCHIVO_SALIDA = "alvaroguia.xml"

def main():
    # Descargamos el XML original tal cual
    r = requests.get(URL_EPG)
    r.encoding = 'utf-8'
    
    # Usamos el parser oficial para mantener la estructura
    root = ET.fromstring(r.text)
    
    # Creamos un nuevo contenedor TV copiando los atributos del original
    nuevo_root = ET.Element("tv")
    for k, v in root.attrib.items():
        nuevo_root.set(k, v)

    # 1. Copiamos los canales (Buscamos los nodos originales para no fallar)
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_INTERES:
            nuevo_root.append(canal)

    # 2. Copiamos los programas
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_INTERES:
            nuevo_root.append(programa)
            
    # Guardamos con el formato EXACTO de epg.ovh
    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        # No ponemos DOCTYPE si el original no lo requiere, vamos a lo básico
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
