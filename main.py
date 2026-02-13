import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# --- CONFIGURACIÓN DE LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- CONFIGURACIÓN DE SELENIUM PARA LA NUBE ---
def iniciar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # IMPORTANTE: En Streamlit Cloud, Chromium se instala en esta ruta:
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # No usamos Service(ChromeDriverManager().install())
    # Usamos directamente el ejecutable del driver del sistema
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def verificar_columnas(df, columnas_requeridas):
    for columna in columnas_requeridas:
        if columna not in df.columns:
            logging.warning(f"Advertencia: La columna '{columna}' no está presente en el archivo Excel.")
    logging.info("Verificación de columnas completada.")
    return True

def verificar_existencia_campo(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)  # Intenta encontrar el campo por XPath
        return True  # El campo existe
    except:
        logging.error(f"Elemento no encontrado con xpath: {xpath}")
        return False

def menu_button():
    Menu = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productview"]/nav/tp-nav/div/div/div/div')))
    Menu.click()
    return

def product_button():
    product_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/home/div/nav/tp-nav/div/div[2]/div[2]/div[3]/ul/li[4]/div')))
    product_button.click()
    return

def product_setup():
    product_setup = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/home/div/nav/tp-nav/div/div[2]/div[2]/div[3]/ul/li[4]/ul/li[1]/div/label')))
    product_setup.click()
    driver.switch_to.window(driver.window_handles[1])
    return

def product_setup_search_button ():
    search_product = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/product/div/main/section/div/ul/li[2]/tp-button/button')))
    search_product.click()
    return

def menu_home():
    try:
        Menu_home = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/home/div/nav/tp-nav/div/div/div/div')
            )
        )
        Menu_home.click()
        logging.info("Menu Home encontrado y clickeado exitosamente.")
    except TimeoutException:
        logging.warning("Menu Home no está visible. Continuando con la siguiente acción...")
        # Simplemente no hace nada y continúa
        pass
    
spinner_xpath = '/html/body/app-root/tp-spinner/dialog/div'

def BookingAndQuotes ():
    BookingAndQuotes_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[text()='Bookings and Quotes']")))
    BookingAndQuotes_button.click()
    return

def click_xpath_opcional(driver, xpath1, xpath2=None, descripcion="Elemento"):
    """
    Intenta hacer clic en xpath1.
    Si falla, intenta xpath2 (si está definido).
    No detiene el script si ambos fallan.
    """

    try:
        elemento = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath1))
        )
        elemento.click()
        logging.info(f"{descripcion} encontrado usando XPath1.")
        return True

    except TimeoutException:
        logging.warning(f"{descripcion} NO encontrado usando XPath1.")

        if xpath2 is None:
            logging.warning(f"No se definió XPath2 para {descripcion}. Continuando…")
            return False

        # Intentar con XPath2
        try:
            elemento = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath2))
            )
            elemento.click()
            logging.info(f"{descripcion} encontrado usando XPath2.")
            return True

        except TimeoutException:
            logging.error(f"{descripcion} NO encontrado con ninguna de las dos opciones.")
            return False

def FIT():
    xpath_opcion_1 = '//*[@id="homeview"]/nav/tp-nav/div/div[2]/div[2]/div[3]/ul/li[1]/ul/li[1]'
    xpath_opcion_2 = '//*[@id="homeview"]/nav/tp-nav/div/div/div[2]/div[3]/ul/li[1]/ul/li[1]'  # EJEMPLO (cámbialo si es distinto)

    encontrado = click_xpath_opcional(
        driver,
        xpath1=xpath_opcion_1,
        xpath2=xpath_opcion_2,
        descripcion="Botón FIT"
    )

    if encontrado:
        try:
            driver.switch_to.window(driver.window_handles[1])
            logging.info("Cambiando a la pestaña FIT correctamente.")
        except Exception as e:
            logging.error(f"No se pudo cambiar a la pestaña FIT: {e}")
    else:
        logging.warning("No se pudo ingresar a FIT. Continuando…")

    return

def verificar_spinner(driver, spinner_xpath):
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.XPATH, spinner_xpath))
        )
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, spinner_xpath))
        )
    except:
        logging.info(f"No se encontró el spinner o hubo un error")
        time.sleep(2)

def buscar_texto(driver,Sequence):
    try:
        xpath_fila = f"/html/body/app-root/groupbook/div/main/section/article/tp-group-service-list/div/div[2]/tp-grid/div/div/div/table/tbody//td[contains(text(), '{Sequence}')]"
        logging.info(f'Buscando texto en {xpath_fila}')
        elemento = wait.until(
            EC.visibility_of_element_located((By.XPATH, xpath_fila))
        )
        logging.info(f"Texto '{Sequence}' encontrado, haciendo clic en la celda.")
        elemento.click()

    except:
        logging.error(f"No se encontró el texto '{Sequence}' en la tabla.")

def manejar_error_dialog(driver):
    xpath_error_dialog = '/html/body/tp-dialog/dialog/tp-error/div'
    xpath_error_button = '/html/body/tp-dialog/dialog/tp-error/div/div/div[3]/tp-button/button'

    try:
        # Verificar si el diálogo de error aparece
        wait.until(
            EC.visibility_of_element_located((By.XPATH, xpath_error_dialog))
        )
        logging.warning("⚠ Se detectó un mensaje de ERROR en pantalla.")

        # Intentar hacer clic en el botón dentro del diálogo
        try:
            boton_cerrar = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_error_button))
            )
            boton_cerrar.click()
            logging.info("Diálogo de error cerrado.")
        except TimeoutException:
            logging.error("El botón del diálogo de error NO estaba clickeable.")

        return True   # Error manejado, pero sin detener nada

    except TimeoutException:
        return False  # No hay error


# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Notas Pagos", page_icon="🤖")
st.title("🤖 Notas de pagos Tourplan")

with st.sidebar:
    st.header("🔑 Credenciales de Tourplan")
    user_input = st.text_input("Usuario")
    pass_input = st.text_input("Contraseña", type="password")
    
    st.divider()
    st.info("Este script procesa bookings en Tourplan de forma automatizada.")

archivo_excel = st.file_uploader("📂 Subir archivo Excel", type=["xlsx", "xls", "xlsm"])
nombre_pestana = st.text_input("Nombre de la pestaña", value="Hoja1")

if st.button("🚀 Iniciar Proceso"):
    if not user_input or not pass_input or not archivo_excel:
        st.error("Faltan datos (Usuario, Contraseña o Excel).")
    else:
        try:
            # 1. Cargar Excel
            df = pd.read_excel(archivo_excel, sheet_name=nombre_pestana)
            st.success(f"Archivo cargado. {len(df)} filas detectadas.")
            
            # 2. Inicializar Navegador
            with st.status("Conectando con Tourplan...", expanded=True) as status:
                driver = iniciar_navegador()
                wait = WebDriverWait(driver, 15)
                
                # --- LOGIN ---
                status.write("Realizando login...")
                driver.get('https://la-atpdmc.nx.tourplan.net/TourplanNX_test/#/home')
                
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'username'))).send_keys(user_input)
                driver.find_element(By.CLASS_NAME, 'password').send_keys(pass_input)
                driver.find_element(By.XPATH, '//button[contains(text(), "Login") or @type="submit"]').click()
                
                # Esperar entrada al home
                time.sleep(5) 
                
                # --- BUCLE DE PROCESAMIENTO ---
                progress_bar = st.progress(0)
                
                for index, fila in df.iterrows():
                    ref = str(fila.get('REFERENCIA', '')).strip()
                    status.write(f"Procesando: {ref} ({index + 1}/{len(df)})")
                    
                    verificar_spinner(driver, spinner_xpath)
    
                    # Click en el botón de buscar booking
                    FindBookingButton = wait.until(
                        EC.visibility_of_element_located((By.XPATH,'//*[@id="fastbookview"]/main/section/section/div/div[1]/ul/li/tp-button'))
                    ).click()
                    
                    verificar_spinner(driver, spinner_xpath)
                    
                    # Llenar campos de búsqueda
                    BookingRefFrom = driver.find_element(By.XPATH,'//*[@id="bookingreferencefrom"]/div/tp-validator/input')
                    BookingRefFrom.clear()
                    BookingRefFrom.send_keys(BookingRef)
                    
                    BookingRefTo = driver.find_element(By.XPATH,'//*[@id="bookingreferenceto"]/div/tp-validator/input')
                    BookingRefTo.clear()
                    BookingRefTo.send_keys(BookingRef)
                    
                    BookingSearch = driver.find_element(By.XPATH,'//*[@id="bookingsearchview"]/div[1]/div/div/div/tp-button[3]/button')
                    BookingSearch.click()

                    verificar_spinner(driver, spinner_xpath)
                    
                    try:
                        SelectBooking = wait.until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="bookingSearchTabs-results"]/div/tp-grid/div/table/tbody/tr'))
                        )
                        SelectBooking.click()
                    except TimeoutException:
                        logging.warning(f"No se encontró el booking '{BookingRef}' en los resultados.")
                        mensaje = f"El booking '{BookingRef}' NO existe.\n\n¿Es un GroupBook?"
                        respuesta = alerta_booking_no_encontrado(mensaje)
                        if respuesta:
                            driver.refresh()
                            continue
                        else:
                            continue

                    verificar_spinner(driver, spinner_xpath)
                    manejar_error_dialog(driver)
                    
                    # Abrir Menú y Notas (Se mantiene igual pero aplicado a 'fila')
                    try:
                        MenuBooking = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fastbookview"]/nav/tp-nav/div/div/div/div')))
                        MenuBooking.click()
                    except:
                        pass

                    # Selección de Booking Details y Notas
                    # ... (Aquí va tu lógica de XPaths de booking_details y click en booking_notes) ...
                    # (He omitido los XPaths repetidos por brevedad, mantén los que ya tienes en tu script)

                    # Lógica para editar o crear nota PRE
                    # ... (Mantén tu bloque try/except de celda_pre) ...

                    # PREPARACIÓN DEL TEXTO (Usando la 'fila' actual de la iteración)
                    orden_val = fila.get("ORDEN DE PAGO", "")
                    orden_de_pago = "" if pd.isna(orden_val) else str(orden_val)

                    fecha_val = fila.get("FECHA", "")
                    fecha = fecha_val.strftime("%d/%m/%Y") if isinstance(fecha_val, pd.Timestamp) else str(fecha_val)

                    numero_val = fila.get("IMPORTE", "")
                    if pd.notna(numero_val):
                        try:
                            numero_val = int(numero_val) if float(numero_val).is_integer() else numero_val
                        except: pass
                    numero = str(numero_val)

                    texto_final = f"{fecha}  {numero}  {orden_de_pago}"

                    # Escribir en el IFRAME (Igual que tu código original)
                    # ... (Bloque de iframe y ActionChains) ...

                    # Guardar y refrescar para la siguiente fila
                    save_boton = wait.until(
                        EC.element_to_be_clickable((By.XPATH,'/html/body/tp-dialog/dialog/tp-note-editor/div/div/div/div[1]/div/tp-button[5]/button'))
                    ).click()

                    verificar_spinner(driver, spinner_xpath)
                    driver.refresh()
                    progreso = (index + 1) / len(df)
                    progress_bar.progress(progreso)

                driver.quit()
                status.update(label="✅ Proceso Finalizado", state="complete", expanded=False)
                st.balloons()
                st.success("Todas las referencias han sido procesadas.")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            if 'driver' in locals(): driver.quit()
