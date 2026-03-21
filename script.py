import requests
import xml.etree.ElementTree as ET

URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] 
ARCHIVO_SALIDA = "alvaroguia.xml"

def main():
    # 1. Obtener el XML original manteniendo la codificación
    r = requests.get(URL_EPG)
    r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    
    # 2. Crear el nuevo elemento raíz COPIANDO los atributos del original
    # (Esto es lo que hace que la app crea que es el mismo servidor)
    nuevo_root = ET.Element("tv")
    for nombre_atrib, valor_atrib in root.attrib.items():
        nuevo_root.set(nombre_atrib, valor_atrib)

    # 3. Filtrar canales (Manteniendo el orden original)
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_INTERES:
            nuevo_root.append(canal)

    # 4. Filtrar programas
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_INTERES:
            nuevo_root.append(programa)
            
    # 5. Guardar con declaración XML estándar
    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
