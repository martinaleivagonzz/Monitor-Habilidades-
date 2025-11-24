import os
import shutil
import glob

print("🔍 BUSCANDO ARCHIVOS CSV EN TU MAC...")

# Buscar en todas las ubicaciones posibles
lugares = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"), 
    os.path.expanduser("~/Desktop/progra"),
    os.path.expanduser("~"),
    "."
]

# Crear carpeta destino
os.makedirs("data/raw/web_scraper", exist_ok=True)

archivos_encontrados = []
for lugar in lugares:
    if os.path.exists(lugar):
        csv_files = glob.glob(os.path.join(lugar, "**", "*.csv"), recursive=True)
        archivos_encontrados.extend(csv_files)

print(f"📄 Se encontraron {len(archivos_encontrados)} archivos CSV:")

# Mover archivos
for archivo in archivos_encontrados:
    nombre = os.path.basename(archivo)
    destino = f"data/raw/web_scraper/{nombre}"
    
    try:
        shutil.copy2(archivo, destino)
        print(f"✅ COPIADO: {nombre}")
    except Exception as e:
        print(f"❌ Error con {nombre}: {e}")

# Verificar resultado
finales = os.listdir("data/raw/web_scraper")
print(f"\n🎉 TERMINADO: {len(finales)} archivos en data/raw/web_scraper/")
for archivo in finales:
    print(f"   📄 {archivo}")

print("\n🚀 ¡AHORA PUEDES EJECUTAR TU ETL!")