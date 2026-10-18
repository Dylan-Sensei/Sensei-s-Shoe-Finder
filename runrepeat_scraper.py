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

modelo_url = "https://runrepeat.com/es/hoka-speedgoat-7"
response_modelo = requests.get(modelo_url)
soup_modelo = BeautifulSoup(response_modelo.text, "html.parser")

print("\n--- HOKA SPEEDGOAT 7 ---")
print("Código:", response_modelo.status_code)

# Función para buscar una característicafilas = soup_modelo.find_all("tr")
filas = soup_modelo.find_all("tr")
print("\nTotal de filas HTML:", len(filas))

palabras_clave = [
    "Peso",
    "Drop",
    "Absorción de impactos en el talón",
    "Retorno de energía en el talón",
    "Pronación",
    "Placa",
    "rocker"
]

for fila in filas:

    celdas = fila.find_all(["th", "td"])

    valores = [
        celda.get_text(" ", strip=True)
        for celda in celdas
    ]

    if valores and any(
       palabra.lower() in vaores[0].lower()
       for palabra in palabra_clave
    ):
       print("\nFila encontrada:", valores)
