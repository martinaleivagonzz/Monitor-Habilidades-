# -*- coding: utf-8 -*-
import pandas as pd
import os
import re

RAW_PATH = "data/raw/jobs_raw.csv"

def extract_data():
    """
    Extrae datos de Web Scraper con manejo robusto de errores
    """
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    
    print("🔹 Extrayendo datos con manejo robusto de errores...")
    
    # Todos los archivos
    all_files = [
        "data/raw/web_scraper/compu1.csv", "data/raw/web_scraper/compu2.csv",
        "data/raw/web_scraper/compu3.csv", "data/raw/web_scraper/compu4.csv", 
        "data/raw/web_scraper/compu5.csv", "data/raw/web_scraper/indeed1.csv",
        "data/raw/web_scraper/indeed2.csv", "data/raw/web_scraper/indeed3.csv",
        "data/raw/web_scraper/indeed4.csv"
    ]
    
    all_data = []
    
    for file_path in all_files:
        try:
            if os.path.exists(file_path):
                print(f"📁 Procesando: {os.path.basename(file_path)}")
                
                # Leer con manejo flexible de errores
                df_temp = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip', engine='python')
                
                # Estandarizar columnas
                df_clean = estandarizar_columnas(df_temp, file_path)
                
                if not df_clean.empty:
                    all_data.append(df_clean)
                    print(f"   ✅ {len(df_clean)} ofertas procesadas")
                else:
                    print(f"   ⚠️  No se pudieron procesar datos")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # Combinar todos los datos
    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        df_final = limpiar_datos_finales(df_final)
    else:
        # Crear DataFrame con estructura mínima
        df_final = pd.DataFrame(columns=["title", "company", "location", "source", "url", 
                                       "experience_text", "salario", "descripcion", "salario_numerico"])
    
    # Guardar
    df_final.to_csv(RAW_PATH, index=False, encoding="utf-8-sig")
    print(f"🎯 {len(df_final)} ofertas extraídas y guardadas en {RAW_PATH}")
    return df_final

def estandarizar_columnas(df, file_path):
    """
    Estandariza columnas de diferentes fuentes
    """
    # Determinar fuente
    source = "Computrabajo" if "compu" in file_path.lower() else "Indeed"
    
    # Crear nuevo DataFrame estandarizado
    df_estandar = pd.DataFrame()
    
    # Mapear columnas existentes a columnas estandarizadas
    mapeo_columnas = {
        'titulo': 'title',
        'empresa': 'company', 
        'ubicacion': 'location',
        'enlace': 'url',
        'descripcion': 'descripcion', 
        'salario': 'salario',
        'experiencia': 'experience_text',
        'web-scraper-start-url': 'url'
    }
    
    # Aplicar mapeo
    for col_orig, col_dest in mapeo_columnas.items():
        if col_orig in df.columns:
            df_estandar[col_dest] = df[col_orig]
    
    # Asegurar columnas mínimas
    if 'title' not in df_estandar.columns and 'titulo' in df.columns:
        df_estandar['title'] = df['titulo']
    
    if 'company' not in df_estandar.columns:
        df_estandar['company'] = "No especificada"
    
    if 'location' not in df_estandar.columns:
        df_estandar['location'] = "Chile"
    
    if 'source' not in df_estandar.columns:
        df_estandar['source'] = source
    
    if 'descripcion' not in df_estandar.columns:
        df_estandar['descripcion'] = ""
    
    if 'salario' not in df_estandar.columns:
        df_estandar['salario'] = ""
    
    if 'experience_text' not in df_estandar.columns:
        df_estandar['experience_text'] = ""
    
    # Extraer salario numérico
    df_estandar['salario_numerico'] = df_estandar['salario'].apply(extraer_salario_numerico)
    
    return df_estandar

def extraer_salario_numerico(salario_text):
    """Convierte texto de salario a número"""
    if pd.isna(salario_text) or not salario_text:
        return 0.0
    
    text = str(salario_text)
    
    # Buscar patrones de salario
    patrones = [
        r'\$?\s*(\d{1,3}(?:\.\d{3})*(?:\.\d{3})*)',  # $1.500.000
        r'\$?\s*(\d{1,3}(?:\,\d{3})*(?:\,\d{3})*)',  # $1,500,000
        r'(\d+)\s*\$',                              # 1500000 $
    ]
    
    for patron in patrones:
        matches = re.findall(patron, text)
        if matches:
            # Tomar el número más grande
            numeros = []
            for match in matches:
                clean_num = re.sub(r'[\.\,]', '', str(match))
                if clean_num.isdigit():
                    numeros.append(int(clean_num))
            
            if numeros:
                return max(numeros)
    
    return 0.0

def limpiar_datos_finales(df):
    """Limpieza final de datos"""
    # Filtrar ofertas con título
    df = df[df['title'].notna() & (df['title'] != '')]
    
    # Limpiar textos
    columnas_texto = ['title', 'company', 'location', 'descripcion', 'salario', 'experience_text']
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=['title', 'descripcion'])
    
    return df

if __name__ == "__main__":
    extract_data()


        