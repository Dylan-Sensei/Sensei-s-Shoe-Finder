import requests
from bs4 import BeautifulSoup

url = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"

response = requests.get(url)
print("Código de respuesta:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print("Página descargada")
print("Título:", soup.title.text)

links = soup.find_all("a", href=True)

modelos = {}


for link in links:
  nombre = link.get_text(strip=True)
  href = link["href"]

  # Solo enlaces internos de RunRepeat
  # Excluimos páginas de catálogo
  if (
    nombre
    and href.startswith("/es/")
    and "/catalogo/" not in href
  ):
    modelos[href] = nombre
  
print("Modelos encontrados:", len(modelos))
for href, nombre in modelos.items():
  print(nombre, "->", href)
