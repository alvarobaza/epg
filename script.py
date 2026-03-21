import requests
import xml.etree.ElementTree as ET

def main():
    URL = "https://epg.ovh/plar.xml"
    CANALES = ["iTVN", "iTVN extra"]
    
    # Descarga limpia
    r = requests.get(URL)
    r.encoding = 'utf-8'
    old_root = ET.fromstring(r.text)
    
    # Nuevo XML con la MISMA cabecera que el original
    new_root = ET.Element("tv")
    for k, v in old_root.attrib.items():
        new_root.set(k, v)

    # 1. Copiar canales
    for canal in old_root.findall("channel"):
        if canal.get("id") in CANALES:
            new_root.append(canal)

    # 2. Copiar programas
    for prog in old_root.findall("programme"):
        if prog.get("channel") in CANALES:
            new_root.append(prog)
            
    # Guardado con formato compatible
    tree = ET.ElementTree(new_root)
    with open("alvaroguia.xml", "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
