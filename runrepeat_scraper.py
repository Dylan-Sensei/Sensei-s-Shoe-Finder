import requests
from bs4 import BeautifulSoup

url = "https://runrepeat.com/es/catalogo/zapatillas-de-running-new"

response = requests.get(url)
print("Código de respuesta:", response.status_code)

Soup = BeautifulSoup(response.text, "html.parser")
print("Página descargada")
print("Título:", soup.title.text)
