import os

def verificar_rutas_correcto():
    """Verifica que las rutas del proyecto estén correctas"""
    
    print("📍 VERIFICANDO RUTAS DEL PROYECTO")
    print("=" * 50)
    
    # Verificar ubicación actual
    print(f"📂 Carpeta actual: {os.getcwd()}")
    print(f"¿Estamos en monitor_habilidades? {'monitor_habilidades' in os.getcwd()}")
    
    # Verificar estructura esencial
    elementos = [
        "data/raw/web_scraper",
        "data/processed", 
        "data/users",
        "etl",
        "skills",
        "main.py",
        "profile.py",
        "scoring.py"
    ]
    
    print("\n🔍 ESTRUCTURA ESENCIAL:")
    for elemento in elementos:
        existe = os.path.exists(elemento)
        status = "✅" if existe else "❌"
        if os.path.isdir(elemento) if "/" in elemento else elemento in ["data", "etl", "skills"]:
            # Es carpeta
            if existe:
                try:
                    archivos = os.listdir(elemento)
                    print(f"   {status} {elemento}/ ({len(archivos)} archivos)")
                except:
                    print(f"   {status} {elemento}/ (acceso denegado)")
            else:
                print(f"   {status} {elemento}/ - NO EXISTE")
        else:
            # Es archivo
            tamaño = os.path.getsize(elemento) if existe else 0
            print(f"   {status} {elemento} ({tamaño} bytes)")
    
    # Verificar archivos CSV en web_scraper
    print("\n📊 DATOS DE WEB SCRAPER:")
    if os.path.exists("data/raw/web_scraper"):
        csv_files = [f for f in os.listdir("data/raw/web_scraper") if f.endswith('.csv')]
        print(f"   📄 Archivos CSV: {len(csv_files)}")
        for f in csv_files[:5]:  # Mostrar primeros 5
            print(f"      - {f}")
        if len(csv_files) > 5:
            print(f"      ... y {len(csv_files) - 5} más")
    
    print("\n💡 INSTRUCCIONES:")
    print("1. Para ejecutar el proyecto: python main.py")
    print("2. Para modo rápido: python main.py --rapido")
    print("3. Asegúrate de estar en: /Users/paulinagonzalez/python/monitor_habilidades/")

# Ejecutar verificación
if __name__ == "__main__":
    verificar_rutas_correcto()

