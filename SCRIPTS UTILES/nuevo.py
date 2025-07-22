from selenium import webdriver

# Configura el controlador de Selenium
driver = webdriver.Chrome()  # o Firefox(), Edge(), etc.

# Abre la página web
driver.get("https://www.wpadictos.com/wp-content/plugins/")

# Espera a que la página cargue completamente
driver.implicitly_wait(10)  # Espera hasta 10 segundos

# Obtiene el contenido de la página
page_source = driver.page_source

# Puedes continuar el scraping con BeautifulSoup si es necesario
from bs4 import BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Haz algo con `soup`, por ejemplo, extraer contenido específico
print(soup.prettify())

# Cierra el navegador
driver.quit()
