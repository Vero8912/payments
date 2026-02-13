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

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Notas Pagos", page_icon="🤖")
st.title("🤖 Notas de pagos Tourplan")

with st.sidebar:
    st.header("🔑 Credenciales de Tourplan")
    user_input = st.text_input("Usuario")
    pass_input = st.text_input("Contraseña", type="password")
    
    st.divider()
    st.info("Este script procesa bookings en Tourplan de forma automatizada.")

archivo_excel = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx", "xls", "xlsm"])
nombre_pestana = st.text_input("Nombre de la pestaña", value="Sheet1")

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
                    
                    # AQUÍ PEGAS TU LÓGICA DE SELENIUM ACTUALIZADA
                    # (Buscar booking, entrar a notas, escribir texto, guardar)
                    # Ejemplo visual:
                    time.sleep(1) # Simulación
                    
                    # Actualizar progreso
                    progreso = (index + 1) / len(df)
                    progress_bar.progress(progreso)

                driver.quit()
                status.update(label="✅ Proceso Finalizado", state="complete", expanded=False)
                st.balloons()
                st.success("Todas las referencias han sido procesadas.")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            if 'driver' in locals(): driver.quit()
