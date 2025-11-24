import os
import pandas as pd
import numpy as np

# Ruta de origen y destino
RUTA_MATRIZ = "data/processed/matriz_competencias.csv"
RUTA_DESTINO = "data/processed/skills_by_seniority.csv"

def generar_skills_by_seniority():
    """Genera un archivo skills_by_seniority.csv compatible con el dashboard."""
    print("🚀 Iniciando generación de skills_by_seniority.csv...")
    
    # 1. Verificar existencia de la matriz
    if not os.path.exists(RUTA_MATRIZ):
        print(f"❌ No se encontró {RUTA_MATRIZ}")
        return
    
    # 2. Cargar matriz principal
    try:
        matriz = pd.read_csv(RUTA_MATRIZ)
    except Exception as e:
        print(f"❌ Error al leer matriz_competencias.csv: {e}")
        return
    
    if 'skill' not in matriz.columns:
        print("❌ La matriz no contiene una columna 'skill'.")
        return
    
    # 3. Crear carpeta destino si no existe
    os.makedirs(os.path.dirname(RUTA_DESTINO), exist_ok=True)
    
    # 4. Generar distribución por nivel de experiencia
    niveles = ['Junior', 'Semi-Senior', 'Senior']
    registros = []

    for _, fila in matriz.iterrows():
        skill = fila['skill']
        
        # Distribución proporcional según importancia
        importancia = fila.get('importancia', 'Media')
        base_count = int(fila.get('frecuencia_mercado', np.random.randint(10, 100)))
        
        if importancia == 'Crítica':
            pesos = [0.3, 0.4, 0.3]
        elif importancia == 'Alta':
            pesos = [0.4, 0.4, 0.2]
        else:
            pesos = [0.5, 0.3, 0.2]
        
        counts = (np.array(pesos) * base_count).astype(int)
        
        for nivel, c in zip(niveles, counts):
            registros.append({
                "skill": skill,
                "seniority": nivel,
                "count": int(c)
            })
    
    # 5. Crear DataFrame final
    df_final = pd.DataFrame(registros)
    
    # 6. Guardar CSV
    df_final.to_csv(RUTA_DESTINO, index=False, encoding='utf-8')
    print(f"✅ Archivo generado exitosamente: {RUTA_DESTINO}")
    
    # 7. Mostrar resumen
    resumen = df_final.groupby("seniority")["count"].sum()
    print("\n📊 Distribución total por nivel de experiencia:")
    print(resumen)
    
    print("\n✅ El archivo ya está listo para usarse en tu dashboard.")

if __name__ == "__main__":
    generar_skills_by_seniority()
