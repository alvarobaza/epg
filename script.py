import requests
import gzip
import xml.etree.ElementTree as ET

def main():
    # 1. Descarga del archivo comprimido de epgshare01
    url = "https://epgshare01.online/epgshare01/epg_ripper_PL1.xml.gz"
    print("Descargando EPG de epgshare01...")
    
    response = requests.get(url, stream=True)
    
    # 2. Descomprimir en memoria
    with gzip.GzipFile(fileobj=response.raw) as f:
        xml_content = f.read()
    
    root = ET.fromstring(xml_content)
    
    # IDs EXACTOS que me has pasado
    CANALES_TARGET = ["iTVN.pl", "iTVN.Extra.International.pl"]
    
    # 3. Crear el nuevo XML con la misma cabecera
    nuevo_root = ET.Element("tv", root.attrib)

    # Filtrar canales
    for canal in root.findall("channel"):
        if canal.get("id") in CANALES_TARGET:
            nuevo_root.append(canal)

    # Filtrar programas
    for programa in root.findall("programme"):
        if programa.get("channel") in CANALES_TARGET:
            nuevo_root.append(programa)

    # 4. Guardado final
    tree = ET.ElementTree(nuevo_root)
    with open("alvaroguia.xml", "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)
    
    print("Archivo alvaroguia.xml generado con éxito.")

if __name__ == "__main__":
    main()
