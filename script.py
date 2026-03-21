import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Configuración
URL_EPG = "https://epg.ovh/plar.xml"
# ID_ORIGINAL -> ID_NUEVO (Solo para el ID técnico)
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
    root = ET.fromstring(r.content)
    
    nuevo_root = ET.Element("tv")
    canales_añadidos = set()
    
    # 1. Procesar Canales
    for canal in root.findall("channel"):
        id_orig = canal.get("id")
        if id_orig in MAPEO_CANALES and id_orig not in canales_añadidos:
            nuevo_id = MAPEO_CANALES[id_orig]
            
            # Creamos el canal con el ID técnico (con 1a_)
            c = ET.Element("channel", id=nuevo_id)
            
            # Mantenemos los nombres ORIGINALES (sin el 1a_) para que se vea bien
            for name in canal.findall("display-name"):
                c.append(name)
            
            # Copiamos el icono
            icon = canal.find("icon")
            if icon is not None:
                c.append(icon)
                
            nuevo_root.append(c)
            canales_añadidos.add(id_orig)
            
    # 2. Procesar Programas
    for programa in root.findall("programme"):
        ch_orig = programa.get("channel")
        if ch_orig in MAPEO_CANALES:
            # Vinculamos el programa al nuevo ID técnico
            p = ET.Element("programme")
            p.set("channel", MAPEO_CANALES[ch_orig])
            p.set("start", corregir_hora(programa.get("start"), OFFSET_HORAS))
            p.set("stop", corregir_hora(programa.get("stop"), OFFSET_HORAS))
            
            # Copiamos el contenido del programa (título, desc, etc.)
            for elem in programa:
                p.append(elem)
                
            nuevo_root.append(p)
            
    # Guardar XML
    tree = ET.ElementTree(nuevo_root)
    tree.write(ARCHIVO_SALIDA, encoding="utf-8", xml_declaration=True)
    print(f"Archivo {ARCHIVO_SALIDA} generado con éxito.")

if __name__ == "__main__":
    main()
