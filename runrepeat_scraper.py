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

#Recorrer páginas 1 2 y 3

for pagina in range(1, 4):
   url = f"{url_base}?page={pagina}"
   print(f"\nAnalizando página {pagina}...")


response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", href=True)

print("Página descargada")
print("Título:", soup.title.text)




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
  
print("\n Total de Modelos encontrados:", len(modelos))

for href, nombre in modelos.items():
  print(nombre, "->", href)
