with open('item_opciones_ejemplo.json', 'r', encoding='utf-8-sig') as f:
    data = f.read()

with open('item_opciones_ejemplo.json', 'w', encoding='utf-8') as f:
    f.write(data)

print("Archivo item_opciones_ejemplo.json reescrito en UTF-8 sin BOM.") 