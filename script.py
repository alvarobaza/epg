import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
MAPEO_CANALES = {
    "iTVN": "1a_iTVN",
    "iTVN extra": "1a_iTVN_extra"
}
OFFSET_HORAS = 6
ARCHIVO_SALIDA = "alvaroguia.xml"

def corregir_hora(timestr, horas):
    formato = "%Y%m%d%H%M%S %z"
    try:
        dt = datetime.strptime(timestr, formato)
        dt_corregida = dt + timedelta(hours=horas)
        return dt_corregida.strftime(formato)
    except:
        return timestr

def main():
    print("Descargando EPG original...")
    r = requests.get(URL_EPG)
    r.encoding = 'utf-8'
    root = ET.fromstring(r.text)
    
    nuevo_root = ET.Element("tv")
    canales_añadidos = set()
    
    # 1. Procesar Canales
    for canal in root.findall("channel"):
        id_orig = canal.get("id")
        if id_orig in MAPEO_CANALES and id_orig not in canales_añadidos:
            nuevo_id = MAPEO_CANALES[id_orig]
            c = ET.SubElement(nuevo_root, "channel", id=nuevo_id)
            
            # Buscamos el display-name original
            for name in canal.findall("display-name"):
                dn = ET.SubElement(c, "display-name", lang=name.get("lang", "pl"))
                dn.text = name.text
            
            icon = canal.find("icon")
            if icon is not None:
                ET.SubElement(c, "icon", src=icon.get("src"))
                
            canales_añadidos.add(id_orig)
            
    # 2. Procesar Programas
    for programa in root.findall("programme"):
        ch_orig = programa.get("channel")
        if ch_orig in MAPEO_CANALES:
            p = ET.SubElement(nuevo_root, "programme")
            p.set("channel", MAPEO_CANALES[ch_orig])
            p.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            p.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            
            for elem in programa:
                child = ET.SubElement(p, elem.tag)
                if elem.text: child.text = elem.text
                for attr_name, attr_value in elem.attrib.items():
                    child.set(attr_name, attr_value)
            
    # Guardar con formato legible (Prettify)
    xml_str = ET.tostring(nuevo_root, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito.")

if __name__ == "__main__":
    main()
