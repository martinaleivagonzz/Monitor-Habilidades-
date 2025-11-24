# scoring.py (corregido)
import json
import pandas as pd
from pathlib import Path
import random
import sys

# =========================================================
# CONFIGURACIÓN DE RUTAS
# =========================================================
DATA_USERS = Path("data/users")
DATA_PROCESSED = Path("data/processed")
RESOURCES_FILE = Path("skills/resources.json")

DATA_USERS.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# =========================================================
# FUNCIÓN: CARGAR PERFIL DE USUARIO
# =========================================================
def load_user_profile(user_id: str):
    file_path = DATA_USERS / f"{user_id}.json"
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el perfil del usuario: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# =========================================================
# FUNCIÓN: CARGAR RECURSOS DE APRENDIZAJE
# =========================================================
def load_resources():
    if not RESOURCES_FILE.exists():
        raise FileNotFoundError("No se encontró el archivo resources.json en /skills")
    with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# =========================================================
# FUNCIÓN: CALCULAR SCORING
# =========================================================
def calculate_scoring(user_profile: dict):
    habilidades = [h.strip() for h in user_profile.get("habilidades", []) if isinstance(h, str) and h.strip()]
    experiencia = user_profile.get("experiencia", "Junior")

    if not habilidades:
        raise ValueError("El perfil no contiene habilidades para analizar.")

    # Generar puntuaciones aleatorias controladas según el nivel
    base = {"Junior": (40, 70), "Semi-Senior": (60, 85), "Senior": (75, 95)}
    rango = base.get(experiencia, (50, 80))

    data = []
    for h in habilidades:
        score = random.randint(*rango)
        if score >= 80:
            categoria = "Alta"
        elif score >= 60:
            categoria = "Próxima"
        else:
            categoria = "Aprender urgente"
        data.append({"Habilidad": h, "Puntuación": score, "Categoría": categoria})

    df = pd.DataFrame(data)
    df.to_csv(DATA_PROCESSED / "skills_by_seniority.csv", index=False)
    return df

# =========================================================
# FUNCIÓN: GENERAR RECOMENDACIONES PERSONALIZADAS
# =========================================================
def generate_recommendations(user_profile: dict, df_scoring: pd.DataFrame):
    resources = load_resources()
    recommendations = {"usuario": user_profile.get("nombre", "Anónimo"), "recomendaciones": []}

    skills_urgentes = df_scoring[df_scoring["Categoría"] == "Aprender urgente"]["Habilidad"].tolist()
    cursos = resources.get("cursos_recomendados", {}).get("gratuitos", []) + \
             resources.get("cursos_recomendados", {}).get("de_pago", [])

    for skill in skills_urgentes:
        for curso in cursos:
            if any(skill.lower() in s.lower() for s in curso.get("skills", [])):
                recommendations["recomendaciones"].append({
                    "habilidad": skill,
                    "curso": curso.get("nombre", ""),
                    "plataforma": curso.get("plataforma", ""),
                    "nivel": curso.get("nivel", ""),
                    "url": curso.get("url", "")
                })

    if not recommendations["recomendaciones"]:
        recommendations["recomendaciones"].append({
            "mensaje": "No se encontraron cursos específicos, revisa las rutas generales en 'Recursos'."
        })

    # Guardar archivo de recomendaciones con user-safe id
    nombre_usuario = user_profile.get("nombre", "usuario")
    safe_userid = str(nombre_usuario).strip().replace(" ", "_").lower() or "usuario"
    rec_file = DATA_PROCESSED / f"recommendations_{safe_userid}.json"
    with open(rec_file, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, indent=4, ensure_ascii=False)

    return recommendations

# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================
def main():
    print("=== Monitor de Habilidades — Cálculo de Scoring ===")
    try:
        user_id = input("Ingresa tu ID de usuario (ej. paula01): ").strip()
        if not user_id:
            print("ID de usuario vacío. Saliendo.")
            return

        print("\nCargando perfil del usuario...")
        user_profile = load_user_profile(user_id)
        print(f"Perfil cargado correctamente ({user_profile.get('nombre', 'Sin nombre')})")

        print("\nCalculando puntuación de habilidades...")
        df = calculate_scoring(user_profile)
        print("✅ Puntuaciones generadas correctamente.\n")

        print("Generando recomendaciones...")
        recs = generate_recommendations(user_profile, df)
        print("✅ Recomendaciones creadas y guardadas.")

        print("\nArchivos generados:")
        csv_path = DATA_PROCESSED / "skills_by_seniority.csv"
        rec_path = DATA_PROCESSED / f"recommendations_{str(user_profile.get('nombre','usuario')).strip().replace(' ', '_').lower()}.json"
        print(" -", csv_path)
        print(" -", rec_path)

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")

def calcular_scoring_completo(user_profile):
    return calculate_scoring(user_profile)



# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================
if __name__ == "__main__":
    main()




