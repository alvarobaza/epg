import requests
import gzip
import io
import xml.etree.ElementTree as ET

def main():
    url = "https://epgshare01.online/epgshare01/epg_ripper_PL1.xml.gz"
    targets = ["iTVN.pl", "iTVN.Extra.International.pl"]
    
    print("Descargando y descomprimiendo fuente...")
    response = requests.get(url)
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
        xml_content = f.read()
    
    root = ET.fromstring(xml_content)
    nuevo_root = ET.Element("tv", root.attrib)

    # Filtrar Canales
    for canal in root.findall("channel"):
        if canal.get("id") in targets:
            nuevo_root.append(canal)

    # Filtrar Programas
    for programa in root.findall("programme"):
        if programa.get("channel") in targets:
            nuevo_root.append(programa)

    # Convertir a texto XML
    xml_str = ET.tostring(nuevo_root, encoding='utf-8')
    
    # GUARDAR COMO .GZ (Comprimido)
    print("Comprimiendo y guardando alvaroguia.xml.gz...")
    with gzip.open("alvaroguia.xml.gz", "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(xml_str)

if __name__ == "__main__":
    main()
