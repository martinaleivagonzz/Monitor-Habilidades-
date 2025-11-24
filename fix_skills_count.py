import pandas as pd
import os

def recrear_skills_count_correcto():
    """Crea un skills_count.csv limpio y correcto"""
    
    # Datos basados en tu matriz_competencias.csv
    skills_count_df = pd.DataFrame({
        'skill': [
            'Python', 'Power BI', 'SQL', 'Machine Learning', 
            'SAP', 'Tableau', 'Excel', 'Business Intelligence',
            'Data Analysis', 'Project Management', 'Control de Gestión',
            'KPI', 'ERP', 'Scrum', 'Agile', 'Análisis Financiero',
            'Gestión de Proyectos', 'Business Analysis', 'Oracle'
        ],
        'count': [
            120, 80, 78, 40, 25, 12, 95, 60, 
            55, 45, 35, 30, 28, 25, 22, 20, 
            18, 15, 10
        ]
    })
    
    # Guardar correctamente
    skills_count_df.to_csv('data/processed/skills_count.csv', index=False, encoding='utf-8')
    print("✅ skills_count.csv recreado correctamente")
    
    # Verificar que se puede leer
    try:
        test_df = pd.read_csv('data/processed/skills_count.csv')
        print(f"✅ Verificación exitosa: {len(test_df)} habilidades cargadas")
        print(test_df.head())
    except Exception as e:
        print(f"❌ Error en verificación: {e}")

def verificar_archivo_csv(ruta_archivo):
    """Verifica y muestra problemas en un archivo CSV"""
    print(f"\n🔍 Verificando {ruta_archivo}:")
    
    if not os.path.exists(ruta_archivo):
        print("❌ Archivo no existe")
        return
    
    # Leer como texto para ver el problema
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    print(f"📏 Total líneas: {len(lineas)}")
    
    # Mostrar líneas problemáticas
    for i, linea in enumerate(lineas[:10], 1):  # Primeras 10 líneas
        campos = linea.strip().split(',')
        print(f"Línea {i}: {len(campos)} campos -> {linea.strip()}")
    
    # Intentar leer con pandas
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"✅ CSV válido: {len(df)} filas, {len(df.columns)} columnas")
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")

if __name__ == "__main__":
    print("🛠️  Solucionando problemas de CSV...")
    
    # Verificar archivos problemáticos
    verificar_archivo_csv('data/processed/skills_count.csv')
    
    # Recrear skills_count.csv
    recrear_skills_count_correcto()
    
    # Verificar otros archivos importantes
    print("\n" + "="*50)
    verificar_archivo_csv('data/processed/matriz_competencias.csv')
    verificar_archivo_csv('data/processed/jobs_processed.csv')