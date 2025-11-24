# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional

USERS_DIR = "data/users"

def inicializar_sistema_usuarios():
    """Inicializa el sistema de multi-usuario"""
    os.makedirs(USERS_DIR, exist_ok=True)
    print(f"✅ Sistema de usuarios inicializado en: {USERS_DIR}")

def crear_perfil_usuario(nombre: str, carrera: str, experiencia_años: int = 0) -> Dict:
    """Crea un nuevo perfil de usuario"""
    
    perfil = {
        "id": nombre.lower().replace(" ", "_"),
        "nombre": nombre,
        "carrera": carrera,
        "experiencia_años": experiencia_años,
        "fecha_creacion": datetime.now().isoformat(),
        "ultima_actualizacion": datetime.now().isoformat(),
        "skills_actuales": [],
        "skills_objetivo": [],
        "objetivos_carrera": [],
        "intereses": [],
        "recomendaciones_generadas": 0,
        "historial_recomendaciones": []
    }
    
    # Guardar perfil
    archivo_perfil = f"{USERS_DIR}/{perfil['id']}.json"
    with open(archivo_perfil, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Perfil creado: {nombre} -> {archivo_perfil}")
    return perfil

def cargar_perfil_usuario(usuario_id: str) -> Optional[Dict]:
    """Carga el perfil de un usuario específico"""
    archivo_perfil = f"{USERS_DIR}/{usuario_id}.json"
    
    try:
        with open(archivo_perfil, "r", encoding="utf-8") as f:
            perfil = json.load(f)
        return perfil
    except FileNotFoundError:
        print(f"❌ Perfil no encontrado: {usuario_id}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error en el archivo del perfil: {usuario_id}")
        return None

def actualizar_perfil_usuario(usuario_id: str, updates: Dict) -> bool:
    """Actualiza el perfil de un usuario"""
    perfil = cargar_perfil_usuario(usuario_id)
    if not perfil:
        return False
    
    # Aplicar actualizaciones
    for key, value in updates.items():
        if key in perfil:
            perfil[key] = value
    
    perfil["ultima_actualizacion"] = datetime.now().isoformat()
    
    # Guardar cambios
    archivo_perfil = f"{USERS_DIR}/{usuario_id}.json"
    with open(archivo_perfil, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Perfil actualizado: {usuario_id}")
    return True

def listar_usuarios() -> List[str]:
    """Lista todos los usuarios disponibles"""
    if not os.path.exists(USERS_DIR):
        return []
    
    usuarios = []
    for archivo in os.listdir(USERS_DIR):
        if archivo.endswith('.json'):
            usuario_id = archivo.replace('.json', '')
            usuarios.append(usuario_id)
    
    return sorted(usuarios)

def agregar_skills_usuario(usuario_id: str, skills: List[str], tipo: str = "actuales"):
    """Agrega skills a un usuario (actuales u objetivo)"""
    perfil = cargar_perfil_usuario(usuario_id)
    if not perfil:
        return False
    
    campo_skills = f"skills_{tipo}"
    if campo_skills not in perfil:
        print(f"❌ Tipo de skills no válido: {tipo}")
        return False
    
    # Agregar skills sin duplicados
    for skill in skills:
        if skill not in perfil[campo_skills]:
            perfil[campo_skills].append(skill)
    
    return actualizar_perfil_usuario(usuario_id, perfil)

def calcular_brecha_skills(usuario_id: str, skills_mercado: pd.DataFrame) -> Dict:
    """Calcula la brecha entre skills del usuario y demanda del mercado"""
    perfil = cargar_perfil_usuario(usuario_id)
    if not perfil:
        return {}
    
    skills_actuales = set(perfil.get("skills_actuales", []))
    skills_objetivo = set(perfil.get("skills_objetivo", []))
    
    # Skills del mercado (top 20)
    skills_demandadas = set(skills_mercado.head(20)['skill'].tolist())
    
    # Análisis de brecha
    brecha = {
        "usuario": usuario_id,
        "skills_que_tiene_y_son_demandadas": list(skills_actuales.intersection(skills_demandadas)),
        "skills_objetivo_demandadas": list(skills_objetivo.intersection(skills_demandadas)),
        "skills_demandadas_que_no_tiene": list(skills_demandadas - skills_actuales),
        "skills_que_tiene_pero_no_son_demandadas": list(skills_actuales - skills_demandadas),
        "total_skills_demandadas": len(skills_demandadas),
        "cobertura_actual": len(skills_actuales.intersection(skills_demandadas)),
        "brecha_total": len(skills_demandadas - skills_actuales)
    }
    
    return brecha

def generar_recomendaciones_personalizadas(usuario_id: str, skills_mercado: pd.DataFrame) -> Dict:
    """Genera recomendaciones personalizadas para un usuario"""
    brecha = calcular_brecha_skills(usuario_id, skills_mercado)
    perfil = cargar_perfil_usuario(usuario_id)
    
    if not brecha or not perfil:
        return {}
    
    # Skills críticas para aprender (demandadas y no las tiene)
    skills_criticas = brecha["skills_demandadas_que_no_tiene"][:5]
    
    # Generar recomendaciones
    recomendaciones = {
        "usuario": usuario_id,
        "fecha_generacion": datetime.now().isoformat(),
        "skills_criticas_para_aprender": skills_criticas,
        "skills_a_reforzar": brecha["skills_que_tiene_y_son_demandadas"][:3],
        "match_con_objetivos": [],
        "acciones_recomendadas": [],
        "proximo_paso": f"Aprender {skills_criticas[0]}" if skills_criticas else "Definir skills objetivo"
    }
    
    # Match con objetivos de carrera
    objetivos = perfil.get("objetivos_carrera", [])
    for objetivo in objetivos:
        if any(skill in objetivo.lower() for skill in ['data', 'analyst']):
            recomendaciones["match_con_objetivos"].append({
                "objetivo": objetivo,
                "skills_recomendadas": ["Python", "SQL", "Power BI", "Análisis de Datos"]
            })
        elif any(skill in objetivo.lower() for skill in ['consultor', 'erp']):
            recomendaciones["match_con_objetivos"].append({
                "objetivo": objetivo,
                "skills_recomendadas": ["SAP", "Oracle", "Gestión de Procesos", "ERP"]
            })
        elif any(skill in objetivo.lower() for skill in ['project', 'manager']):
            recomendaciones["match_con_objetivos"].append({
                "objetivo": objetivo,
                "skills_recomendadas": ["Project Management", "Scrum", "Gestión de Presupuestos", "Liderazgo"]
            })
    
    # Acciones recomendadas
    if skills_criticas:
        recomendaciones["acciones_recomendadas"] = [
            f"Curso/certificación en {skill}" for skill in skills_criticas[:3]
        ]
    
    # Guardar en el historial del usuario
    perfil["recomendaciones_generadas"] = perfil.get("recomendaciones_generadas", 0) + 1
    perfil["historial_recomendaciones"].append(recomendaciones)
    
    # Mantener solo las últimas 10 recomendaciones
    if len(perfil["historial_recomendaciones"]) > 10:
        perfil["historial_recomendaciones"] = perfil["historial_recomendaciones"][-10:]
    
    actualizar_perfil_usuario(usuario_id, perfil)
    
    return recomendaciones

# FUNCIONES DE INTERFAZ PARA EL USUARIO
def menu_crear_usuario():
    """Interfaz para crear nuevo usuario"""
    print("\n👤 CREAR NUEVO USUARIO")
    print("=" * 30)
    
    nombre = input("Nombre: ").strip()
    carrera = input("Carrera: ").strip()
    experiencia = input("Años de experiencia (0): ").strip()
    experiencia_años = int(experiencia) if experiencia.isdigit() else 0
    
    perfil = crear_perfil_usuario(nombre, carrera, experiencia_años)
    
    # Preguntar por skills iniciales
    print("\n💡 ¿Quieres agregar skills actuales? (ej: Excel, Python, SQL)")
    skills_input = input("Skills separadas por coma (enter para saltar): ").strip()
    if skills_input:
        skills = [s.strip() for s in skills_input.split(",")]
        agregar_skills_usuario(perfil["id"], skills, "actuales")
    
    print("\n💡 ¿Skills que quieres aprender?")
    skills_objetivo_input = input("Skills separadas por coma (enter para saltar): ").strip()
    if skills_objetivo_input:
        skills_objetivo = [s.strip() for s in skills_objetivo_input.split(",")]
        agregar_skills_usuario(perfil["id"], skills_objetivo, "objetivo")
    
    print(f"\n🎉 Usuario {nombre} creado exitosamente!")
    return perfil["id"]

def menu_seleccionar_usuario():
    """Interfaz para seleccionar usuario existente"""
    usuarios = listar_usuarios()
    
    if not usuarios:
        print("❌ No hay usuarios registrados")
        return None
    
    print("\n👥 SELECCIONAR USUARIO")
    print("=" * 25)
    
    for i, usuario_id in enumerate(usuarios, 1):
        perfil = cargar_perfil_usuario(usuario_id)
        nombre = perfil.get("nombre", usuario_id) if perfil else usuario_id
        print(f"  {i}. {nombre} ({usuario_id})")
    
    print(f"  {len(usuarios) + 1}. Crear nuevo usuario")
    
    try:
        opcion = int(input("\nSelecciona una opción: "))
        if 1 <= opcion <= len(usuarios):
            return usuarios[opcion - 1]
        elif opcion == len(usuarios) + 1:
            return menu_crear_usuario()
        else:
            print("❌ Opción inválida")
            return None
    except ValueError:
        print("❌ Ingresa un número válido")
        return None

# INICIALIZACIÓN AL IMPORTAR
inicializar_sistema_usuarios()

if __name__ == "__main__":
    # Prueba del sistema
    print("🧪 TEST SISTEMA MULTI-USUARIO")
    
    # Crear usuario de prueba si no existe
    if not listar_usuarios():
        crear_perfil_usuario("Usuario Demo", "Ingeniería", 2)
    
    usuarios = listar_usuarios()
    print(f"👥 Usuarios registrados: {usuarios}")
    
    

  
    
           
        

