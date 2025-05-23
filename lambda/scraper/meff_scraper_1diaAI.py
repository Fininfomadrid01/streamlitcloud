import pandas as pd
from typing import Union, Tuple, Dict, List
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select

MEFF_URL = "https://www.meff.es/esp/Derivados-Financieros/Ficha/FIEM_MiniIbex_35"

def setup_driver() -> webdriver.Chrome:
    """Inicializa y devuelve un WebDriver de Chrome para Selenium."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Descomentar para modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    try:
        print("Inicializando Chrome WebDriver...")
        driver = webdriver.Chrome(options=options)
        print("WebDriver inicializado.")
        return driver
    except Exception as e:
        print(f"Error al inicializar WebDriver: {e}")
        raise

def accept_cookies(driver: webdriver.Chrome):
    """Encuentra y clica el botón 'Aceptar todas' del banner de cookies."""
    button_id = "onetrust-accept-btn-handler"
    try:
        print("Buscando banner de cookies...")
        btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, button_id))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.5)
        try:
            btn.click()
        except:
            driver.execute_script("arguments[0].click();", btn)
        print("Cookies aceptadas.")
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "onetrust-banner-sdk"))
        )
    except Exception:
        print("No se pudo interactuar con el banner de cookies; se continúa.")

def parse_tables_from_html(html: str) -> Tuple[
    Union[pd.DataFrame, None],
    Union[pd.DataFrame, None],
    Union[pd.DataFrame, None]
]:
    """
    Parsea tablas de futuros, calls y puts desde el HTML usando pandas.read_html.
    """
    futures_df, calls_df, puts_df = None, None, None
    fid = "Contenido_Contenido_tblFuturos"
    cid = "tblOpciones"  # la misma tabla cambia contenido segun sea Call o Put

    try:
        if f'id="{fid}"' in html:
            lst = pd.read_html(html, attrs={'id': fid}, header=0)
            futures_df = lst[0] if lst else None
            print(f"  Tabla Futuros parseada ({len(futures_df) if futures_df is not None else 0} filas)")
        if f'id="{cid}"' in html:
            lst = pd.read_html(html, attrs={'id': cid}, header=0)
            calls_df = lst[0] if lst else None
            puts_df  = calls_df
            print(f"  Tabla Opciones parseada ({len(calls_df) if calls_df is not None else 0} filas)")
    except Exception as e:
        print(f"Error al parsear tablas: {e}")

    return futures_df, calls_df, puts_df

def scrape_meff_data_selenium() -> Tuple[
    Dict[str, pd.DataFrame],
    Dict[str, pd.DataFrame],
    Dict[str, pd.DataFrame]
]:
    """
    Scrapea datos SOLO para la fecha por defecto:
    1) Acepta cookies
    2) Espera a la tabla de futuros
    3) Parsea HTML para Futuros, Calls y Puts
    """
    driver = None
    all_futures, all_calls, all_puts = {}, {}, {}
    key = "Default Date"

    try:
        driver = setup_driver()
        driver.get(MEFF_URL)
        accept_cookies(driver)

        # Esperar a que aparezca la tabla de futuros
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "Contenido_Contenido_tblFuturos"))
        )
        time.sleep(1.5)

        html = driver.page_source
        f_df, c_df, p_df = parse_tables_from_html(html)

        if f_df is not None: all_futures[key] = f_df
        if c_df is not None: all_calls[key]   = c_df
        if p_df is not None: all_puts[key]    = p_df

    except Exception as e:
        print(f"Error crítico en scraper: {e}")
    finally:
        if driver:
            try:
                print("--- Browser Console Logs ---")
                for entry in driver.get_log('browser'):
                    print(f"[{entry['level']}] {entry['message']}")
            except:
                pass
            driver.quit()

    return all_futures, all_calls, all_puts

# --- Main execution block for testing ---
if __name__ == "__main__":
    start = time.time()
    # Llamamos al scraper de la fecha por defecto
    futures, calls, puts = scrape_meff_data_selenium()
    end = time.time()

    print(f"\n--- Resumen de Scraping (Default Date Only) ---")
    print(f"Execution time: {end - start:.2f} seconds\n")

    key = "Default Date"
    # Imprimir tabla de futuros
    if key in futures:
        print("Futuros encontrados para la fecha por defecto:")
        print(futures[key].to_string(index=False), "\n")
    else:
        print("No se encontraron datos de futuros.\n")

    # Imprimir opciones Call
    if key in calls:
        print("Opciones Call encontradas:")
        print(calls[key].to_string(index=False), "\n")
    else:
        print("No se encontraron datos de opciones Call.\n")

    # Imprimir opciones Put
    if key in puts:
        print("Opciones Put encontradas:")
        print(puts[key].to_string(index=False), "\n")
    else:
        print("No se encontraron datos de opciones Put.\n")