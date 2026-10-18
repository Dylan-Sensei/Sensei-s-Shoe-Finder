import requests
from bs4 import BeautifulSoup

url_base = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"

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

# Función para buscar una característicafilas = soup_modelo.find_all("tr")
filas = soup_modelo.find_all("tr")
print("\nTotal de filas HTML:", len(filas))

palabras_clave = [
    "Peso",
    "Drop",
    "Absorción de impactos en el talón",
    "Retorno de energía",
    "Pronación",
    "Placa",
    "rocker"
]

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

    if valores and any(
       palabra.lower() in valores[0].lower()
       for palabra in palabras_clave
    ):
       print("\nFila encontrada:", valores)
       
print("\n--- PLACA Y ROCKER---")
for fila in soup_modelo.find_all("tr"):
   celdas=fila.find_all(["th","td"])
   valores=[
      celda.get_text(" ",strip=True)
      for celda in celdas
   ]
   if len(valores) >=2:
      etiqueta=valores[0].lower().strip()
      if etiqueta == "placa":
         tipo_placa, placa_carbono = clasificar+placa(valores[1])
         print("Tipo de placa:", tipo_placa)
         print("Placa de carbono:",placa_carbono)
      elif eiqueta =="con rocker":
         valor_rocker = valores[1].lower().strip()

         if valor_rocker in ["✓", "✔", "sí", "si"]:
             rocker = 1

         elif valor_rocker in ["x", "✗", "✕", "no"]:
             rocker = 0

         else:
             rocker = None

         print("Rocker:", rocker)
