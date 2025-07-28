import webbrowser
import time

def abrir_links_en_chrome(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        links = [line.strip() for line in file if line.strip()]

    chrome_path = webbrowser.get(using='windows-default')  # O usa el path directo si querés
    for link in links:
        chrome_path.open_new_tab(link)
        time.sleep(0.5)  # Espera medio segundo entre pestañas para no saturar

    print("✅ Todos los links fueron abiertos en Chrome.")

# Uso
abrir_links_en_chrome("whatsapplinks.txt")
