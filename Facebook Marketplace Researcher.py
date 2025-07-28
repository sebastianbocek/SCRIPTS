import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def main(producto):
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.facebook.com/marketplace/104099769626471/")

        wait = WebDriverWait(driver, 15)
        # Espera para que cargues sesión manualmente (mejor usar perfil guardado)
        time.sleep(15)

        busqueda = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Buscar en Marketplace"]')))
        busqueda.send_keys(producto)
        busqueda.send_keys(Keys.ENTER)

        time.sleep(5)  # Esperar resultados

        resultados = driver.find_elements(By.CSS_SELECTOR, "a[href*='/marketplace/item/']")

        productos = []

        for item in resultados[:20]:
            try:
                titulo = item.text
                url = item.get_attribute("href")
                precio_element = item.find_element(By.XPATH, ".//span[contains(text(),'$')]")
                precio_text = precio_element.text
                precio_num = float(re.sub(r'[^\d.]', '', precio_text))
                productos.append({"titulo": titulo, "url": url, "precio": precio_num})
            except Exception:
                continue

        productos_ordenados = sorted(productos, key=lambda x: x["precio"])

        print("Mejores opciones por precio más bajo:")
        for p in productos_ordenados[:10]:
            print(f"{p['titulo']} - ${p['precio']}")
            print(f"Link: {p['url']}\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buscador Facebook Marketplace con Selenium")
    parser.add_argument("-p", "--producto", type=str, required=True, help="Producto a buscar")
    args = parser.parse_args()

    main(args.producto)
