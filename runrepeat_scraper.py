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

modelo_url = "https://runrepeat.com/es/nike-zoom-fly-6"
response_modelo = requests.get(modelo_url)
soup_modelo = BeautifulSoup(response_modelo.text, "html.parser")

print("\n--- NIKE ZOOM FLY 6 ---")
print("Código:", response_modelo.status_code)

# Función para buscar una característica
filas = soup_modelo.find_all("tr")
print("\nTotal de filas HTML:", len(filas))

import re
# Creamos un diccionario del Modelo para recuperar las metricas de los tenis en un formato extraible para Sheets

datos_modelo = {
   "modelo": "Nike Zoom Fly 6",
   "url":modelo_url,
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
def extraer_numero(texto,patron):
   coincidencia = re.search(patron,texto,re.IGNORECASE)
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
       peso = extraer_numero(valor, r"\((\d+(?:[.,]\d+)?)\s*g\)")
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


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

print("\n--- DATOS DEL MODELO ---")

for campo, valor in datos_modelo.items():
    print(f"{campo}: {valor}")
       
