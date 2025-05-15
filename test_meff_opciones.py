import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def clean_value(val):
    if isinstance(val, str):
        val = val.replace('&nbsp;', '').strip()
    return val

def clean_and_convert(val):
    if val in ('-', '', None):
        return None
    val = val.replace('.', '').replace(',', '.')
    try:
        return float(val)
    except ValueError:
        return None

def obtener_datos_meff():
    url = 'https://www.meff.es/esp/Derivados-Financieros/Ficha/FIEM_MiniIbex_35'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 1. Mapear vencimientos
    options = soup.select('select.form-control option')
    vencimientos = {opt['value']: opt.text.strip() for opt in options}
    print("Vencimientos encontrados en el desplegable:", vencimientos)

    # 2. Opciones
    rows_opciones = soup.select('table#tblOpciones tbody tr[data-tipo]')
    data_opciones = []

    for row in rows_opciones:
        data_tipo = row['data-tipo']
        vencimiento_str = vencimientos.get(data_tipo, None)
        print(f"data_tipo: {data_tipo}, vencimiento_str: {vencimiento_str}")

        # Fallback: intenta corregir si es OPE / OCE issue
        if vencimiento_str is None:
            data_tipo_clean = data_tipo.replace('OPE', 'OCE') if 'OPE' in data_tipo else data_tipo
            vencimiento_str = vencimientos.get(data_tipo_clean, None)

        cols = row.find_all('td')
        if not cols or len(cols) < 2:
            continue

        strike = clean_value(cols[0].text)
        ant = clean_value(cols[-1].text)
        type_opt = 'CALL' if data_tipo[1] == 'C' else 'PUT'

        data_opciones.append([strike, ant, vencimiento_str, type_opt])

    df_opciones = pd.DataFrame(data_opciones, columns=['Strike', 'Anterior', 'Vencimiento', 'Tipo'])
    df_opciones['Vencimiento'] = pd.to_datetime(df_opciones['Vencimiento'], format='%d/%m/%Y', errors='coerce')
    df_opciones['Strike'] = df_opciones['Strike'].apply(clean_and_convert)
    df_opciones['Anterior'] = df_opciones['Anterior'].apply(clean_and_convert)

    return df_opciones

if __name__ == "__main__":
    df_opciones = obtener_datos_meff()
    print("\nPrimeras filas del DataFrame de opciones:")
    print(df_opciones.head(20))
    print("\nVencimientos únicos encontrados en el DataFrame:")
    print(df_opciones['Vencimiento'].dropna().unique()) 