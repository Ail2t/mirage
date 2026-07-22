import requests

from bs4 import BeautifulSoup

url = "http://localhost:4280/"
response = requests.get(url, timeout=10)
html = response.text
soup = BeautifulSoup(html, "html.parser")

token = soup.find("input", attrs={"name": "user_token"})["value"]

print(token)
