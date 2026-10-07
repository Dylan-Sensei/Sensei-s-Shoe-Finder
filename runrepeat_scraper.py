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

print("\n--- PRUEBA MODELO INDIVIDUAL ---")
print("Código:", response_modelo.status_code)
print("Título:", soup_modelo.title.text)

texto = soup_modelo.get_text(" ", strip=True)

palabras_clave = [
   "Peso",
    "Drop",
    "Absorción",
    "Retorno",
    "Estabilidad",
    "Rigidez",
    "Anchura",
    "Altura",
    "Suela",
    "Técnica de carrera",
    "Placa",
    "Rocker",
    "Prnación"
]

for palabra in palabras_clave:
   posicion = texto.lower().find(palabra.lower())
   if posicion != -1:
      print(f"\n --- {palabra} ---")
      print(texto[posicion:posicion + 500])
