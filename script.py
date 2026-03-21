import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
# Mapeo: ID Original del EPG -> Nuevo ID para tu búsqueda
MAPEO = {
    "iTVN": "ALVAROiTVN",
    "iTVN extra": "ALVAROiTVNextra"
}
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "alvaroguia.xml"

def corregir_hora(timestr, horas):
    formato = "%Y%m%d%H%M%S %z"
    try:
        dt = datetime.strptime(timestr, formato)
        dt_corregida = dt + timedelta(hours=horas)
        return dt_corregida.strftime(formato)
    except: return timestr

def main():
    r = requests.get(URL_EPG)
    root = ET.fromstring(r.content)
    
    nuevo_root = ET.Element("tv")

    # 1. Definir los canales con los nuevos nombres pegados
    for id_orig, nuevo_id in MAPEO.items():
        c = ET.SubElement(nuevo_root, "channel", id=nuevo_id)
        d = ET.SubElement(c, "display-name")
        d.text = nuevo_id # Esto es lo que escribirás en el buscador

    # 2. Asignar programas
    for programa in root.findall("programme"):
        ch_orig = programa.get("channel")
        if ch_orig in MAPEO:
            nuevo_id = MAPEO[ch_orig]
            p = ET.SubElement(nuevo_root, "programme", channel=nuevo_id)
            p.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            p.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            for elem in programa:
                child = ET.SubElement(p, elem.tag)
                child.text = elem.text
                for k, v in elem.attrib.items(): child.set(k, v)

    tree = ET.ElementTree(nuevo_root)
    with open(ARCHIVO_SALIDA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    main()
