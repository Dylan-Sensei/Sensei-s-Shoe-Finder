import requests
from bs4 import BeautifulSoup

url = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"

response = requests.get(url)
print("Código de respuesta:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print("Página descargada")
print("Título:", soup.title.text)

links = soup.find_all("a", href=True)

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
  
print("Modelos encontrados:", len(modelos))

for href, nombre in modelos.items():
  print(nombre, "->", href)
