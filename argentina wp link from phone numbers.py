def convertir_a_whatsapp_links(input_txt, output_txt):
    with open(input_txt, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_txt, 'w', encoding='utf-8') as outfile:
        for line in lines:
            numero = line.strip()
            if numero.lower() == "phone" or not numero:
                continue
            # Limpiar el número: eliminar espacios y guiones
            limpio = numero.replace(" ", "").replace("-", "")
            # Eliminar el primer 0 si existe
            if limpio.startswith("0"):
                limpio = limpio[1:]
            # Agregar el prefijo internacional de Argentina
            link = f"https://api.whatsapp.com/send/?phone=549{limpio}&text&type=phone_number&app_absent=0"
            outfile.write(link + "\n")

    print(f"✅ Links de WhatsApp guardados en {output_txt}")

# Uso de ejemplo
convertir_a_whatsapp_links("phonenumbers.txt", "whatsapplinks.txt")
