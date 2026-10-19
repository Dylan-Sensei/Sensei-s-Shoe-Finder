#Importamos las librerias
import requests
from bs4 import BeautifulSoup
#esta es la pagina de base de datos para el scrapper
url_base = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"
#determinamos que marcasd e tenis queremos recuperar de RUNREPEAT
marcas = [
   "HOKA",
    "ASICS",
    "New Balance",
    "Brooks",
    "Altra",
    "PUMA",
    "adidas",
    "On",
    "Saucony",
    "Skechers",
    "Mount to Coast",
    "Topo",
    "Vivobarefoot",
    "Nike",
    "La Sportiva",
    "Salomon",
    "Merrell"
]

modelos = {}

#Recorrer páginas indefinidamente
pagina = 1
while True:

   url = f"{url_base}?page={pagina}"
   print(f"\nAnalizando página {pagina}...")


   response = requests.get(url)

   soup = BeautifulSoup(response.text, "html.parser")
   print("URL final:", response.url)
   print("Código:", response.status_code)
  
   links = soup.find_all("a", href=True)

   modelos_antes = len(modelos)

   for link in links:
     nombre = link.get_text(strip=True)
     href = link["href"]

  # Solo enlaces internos de RunRepeat
  # Extraemos solo links que tengan nombres de modelos y marcas de tenis
     if (
       nombre
       and href.startswith("/es/")
       and any(nombre.lower().startswith(marca.lower()) for marca in marcas)
     ):
       modelos[href] = nombre
   modelos_nuevos = len(modelos) - modelos_antes  
   print("\n Modelos nuevos:", modelos_nuevos)

#Si no hay modelos nuevos, detener el scrapper
   if modelos_nuevos == 0:
      print("No hay más modelos nuevos")
      break
   pagina += 1

print("\n Total de Modelos encontrados:", len(modelos))
for href, nombre in modelos.items():
  print(nombre, "->", href)

import re
import time

def extraer_numero(texto, patron):
   coincidencia = re.search(patron, texto, re.IGNORECASE)
   if coincidencia:
      return float(coincidencia.group(1).replace(",","."))
   return None
def clasificar_placa(valor):

    valor = valor.lower().strip()

    if "carbono" in valor or "carbon" in valor:
        return "CARBONO", 1

    elif "rock plate" in valor or "rockplate" in valor:
        return "ROCK PLATE", 0

    elif "nylon" in valor or "tpu" in valor:
        return "OTRA PLACA", 0

    elif valor in ["x", "✗", "✕", "no", "sin placa"]:
        return "SIN PLACA", 0

    else:
        return "NO IDENTIFICADO", None

#Funcion principal de Extraccion

def extraer_datos_modelo(url, nombre):
   print(f"\nAnalizando modelo: {nombre}")
   response = requests.get(url,timeout=20)
   response.raise_for_status()
   soup_modelo = BeautifulSoup(response.text,"html.parser")
   filas = soup_modelo.find_all("tr")

   datos_modelo = {
      "modelo": nombre,
      "url":url,
      "peso_lab_g": None,
      "peso_marca_g": None,
      "drop_lab_mm": None,
      "drop_marca_mm": None,
      "absorcion_talon_sa": None,
      "retorno_antepie_pct": None,
      "tipo_placa": None,
      "placa_carbono": None,
      "rocker": None,
      "pronacion": None
   }

   for fila in filas:
      celdas = fila.find_all(["th", "td"])
      valores = [
        celda.get_text(" ", strip=True)
        for celda in celdas
      ]

    if len(valores) <2:
       continue
    etiqueta=valores[0].lower().strip()
    valor=valores[1]

    # Peso de laboratorio
    if etiqueta == "peso":
       peso = extraer_numero(valor, r"\((\d+(?:[.,]\d+)?)\s*g\b)")
       if peso is not None:
           datos_modelo["peso_lab_g"] = peso

    # Peso del fabricante
    elif etiqueta == "peso:":
       datos_modelo["peso_marca_g"] = extraer_numero(
           valor, r"hombre:\s*[\d.,]+\s*oz\s*/\s*(\d+(?:[.,]\d+)?)\s*g"
       )

    # Drop de laboratorio
    elif etiqueta == "drop":
       datos_modelo["drop_lab_mm"] = extraer_numero(
           valor, r"(\d+(?:[.,]\d+)?)\s*mm"
       )
    # Drop del fabricante
    elif etiqueta == "drop:":
       datos_modelo["drop_marca_mm"] = extraer_numero(
           valor, r"(\d+(?:[.,]\d+)?)\s*mm"
       )
    # Absorción de impactos
    elif etiqueta == "absorción de impactos en el talón":
       datos_modelo["absorcion_talon_sa"] = extraer_numero(
           valor, r"(\d+(?:[.,]\d+)?)\s*SA"
       )
    # Retorno de energía
    elif etiqueta == "retorno de energía en el antepié":
       datos_modelo["retorno_antepie_pct"] = extraer_numero(
           valor, r"(\d+(?:[.,]\d+)?)\s*%"
       )
    # Pronación
    elif etiqueta == "pronación:":
       datos_modelo["pronacion"] = valor
    # Placa
    elif etiqueta == "placa":
       tipo_placa, placa_carbono = clasificar_placa(valor)
       datos_modelo["tipo_placa"] = tipo_placa
       datos_modelo["placa_carbono"] = placa_carbono

    # Rocker
    elif etiqueta == "con rocker":
       if valor.lower().strip() in ["✓", "✔", "sí", "si"]:
           datos_modelo["rocker"] = 1

       elif valor.lower().strip() in ["x", "✗", "✕", "no"]:
           datos_modelo["rocker"] = 0

   return datos_modelo


modelos_prueba = [
    ("Nike Zoom Fly 6", "/es/nike-zoom-fly-6"),
    ("HOKA Speedgoat 7", "/es/hoka-speedgoat-7"),
    ("ASICS Novablast 6", "/es/asics-novablast-6"),
    ("Salomon Ultra Glide 4", "/es/salomon-ultra-glide-4"),
    ("adidas Adizero Adios Pro 4", "/es/adidas-adizero-adios-pro-4")
]
resultados = []
for nombre, href in modelos_prueba:

    url = "https://runrepeat.com" + href

    try:
        datos = extraer_datos_modelo(url, nombre)
        resultados.append(datos)

        print("\n--- DATOS EXTRAÍDOS ---")
        for campo, valor in datos.items():
            print(f"{campo}: {valor}")

    except requests.RequestException as error:
        print(f"Error al consultar {nombre}: {error}")

    time.sleep(2)

print("\n--- RESUMEN DE EXTRACCIÓN ---")
print("Modelos procesados:", len(resultados))

for datos in resultados:
    campos_faltantes = [
        campo for campo, valor in datos.items()
        if valor is None
    ]

    print(
        datos["modelo"],
        "| Campos faltantes:",
        campos_faltantes
    )

