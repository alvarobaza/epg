import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

def main():
    URL = "https://epg.ovh/plar.xml"
    CANALES = ["iTVN", "iTVN extra"]
    
    r = requests.get(URL)
    r.encoding = 'utf-8'
    old_root = ET.fromstring(r.text)
    
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
            
    # CONVERTIR A TEXTO CON FORMATO (Prettify)
    xml_str = ET.tostring(new_root, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    with open("alvaroguia.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    main()
