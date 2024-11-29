import requests
from xml.etree import ElementTree

# Endpoint de la API de arXiv
url = "http://export.arxiv.org/api/query"

# Parámetros de búsqueda
params = {
    "search_query": "cat:cs.AI",  # Categoría: Inteligencia Artificial
    "start": 0,  # Índice inicial
    "max_results": 5  # Número máximo de resultados
}

# Realizar la solicitud a la API
response = requests.get(url, params=params)

# Procesar la respuesta
if response.status_code == 200:
    root = ElementTree.fromstring(response.content)
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        link = entry.find("{http://www.w3.org/2005/Atom}id").text
        print(f"Title: {title}\nSummary: {summary}\nLink: {link}\n")
else:
    print(f"Error: {response.status_code}")