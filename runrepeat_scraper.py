import requests
from bs4 import BeautifulSoup

url = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"

response = requests.get(url)
print("Código de respuesta:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print("Página descargada")
print("Título:", soup.title.text)

links = soup.find_all("a", href=True)

print("total de enlaces encontrados:", len(links))

for link in links:
  print(link.get_text(strip=True), "->", link["href"])
