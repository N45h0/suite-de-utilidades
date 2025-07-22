# Script de ejemplo para abrir una página web con Selenium y obtener su contenido HTML

from selenium import webdriver
from bs4 import BeautifulSoup

# Configura el controlador de Selenium
# Asegúrate de tener el driver correspondiente instalado (por ejemplo, chromedriver)
driver = webdriver.Chrome()
driver.get("https://www.wpadictos.com/wp-content/plugins/")
driver.implicitly_wait(10)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
print(soup.prettify())
driver.quit()
