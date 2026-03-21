import requests
import xml.etree.ElementTree as ET

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
CANALES_INTERES = ["iTVN", "iTVN extra"] 
ARCHIVO_SALIDA = "alvaroguia.xml"

def main():
    print("Descargando EPG...")
    r = requests.get(URL_EPG)
    r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    
    # Creamos el nuevo ROOT
    nuevo_root = ET.Element("tv")

    # 1. Reconstruir Canales
    for canal in root.findall("channel"):
        id_canal = canal.get("id")
        if id_canal in CANALES_INTERES:
            # Creamos un nodo nuevo limpio
            c = ET.SubElement(nuevo_root, "channel", id=id_canal)
            for dname in canal.findall("display-name"):
                dn = ET.SubElement(c, "display-name", lang=dname.get("lang", "pl"))
                dn.text = dname.text
            icon = canal.find("icon")
            if icon is not None:
                ET.SubElement(c, "icon", src=icon.get("src"))

    # 2. Reconstruir Programas (Sin tocar horas)
    for programa in root.findall("programme"):
        ch_id = programa.get("channel")
        if ch_id in CANALES_INTERES:
            # Copiamos el programa tal cual
            nuevo_root.append(programa)
            
    # Guardar con la cabecera XML que exigen los reproductores
    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)
    print("Archivo generado.")

if __name__ == "__main__":
    main()
