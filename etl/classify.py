# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def classify_skills_advanced(df: pd.DataFrame) -> Dict:
    """
    Clasificación avanzada de skills por categorías y seniority
    """
    print("🎯 Clasificando skills avanzadamente...")
    
    # Categorías de skills
    categorias = {
        "Tecnologías ERP": ["SAP", "Oracle", "ERP", "Microsoft Dynamics"],
        "Business Intelligence": ["Power BI", "Tableau", "Qlik", "Business Intelligence"],
        "Lenguajes Programación": ["Python", "R", "SQL", "Java", "JavaScript"],
        "Gestión Proyectos": ["Project Management", "Scrum", "Agile", "Kanban", "PMP"],
        "Control Gestión": ["Control de Gestión", "KPI", "Dashboard", "Presupuesto", "Análisis Financiero"],
        "Análisis Datos": ["Machine Learning", "Data Analysis", "Excel", "Big Data"],
        "Cloud & DevOps": ["AWS", "Azure", "GCP", "API"],
        "Habilidades Blandas": ["Liderazgo", "Comunicación", "Inglés"]
    }
    
    # Clasificar cada skill
    classification_results = {
        "categorias": {},
        "seniority_analysis": {},
        "skill_clusters": {},
        "market_trends": {}
    }
    
    # Análisis por categoría
    for categoria, skills in categorias.items():
        skills_en_categoria = []
        for skill in skills:
            if skill in df['skill'].values:
                skill_data = df[df['skill'] == skill]
                if not skill_data.empty:
                    skills_en_categoria.append({
                        'skill': skill,
                        'frecuencia': int(skill_data['frecuencia'].iloc[0]),
                        'porcentaje': float(skill_data['porcentaje'].iloc[0])
                    })
        
        if skills_en_categoria:
            classification_results["categorias"][categoria] = {
                'total_skills': len(skills_en_categoria),
                'total_frecuencia': sum(s['frecuencia'] for s in skills_en_categoria),
                'skills': sorted(skills_en_categoria, key=lambda x: x['frecuencia'], reverse=True)
            }
    
    # Análisis de seniority implícito
    seniority_keywords = {
        "Senior": ["senior", "experto", "avanzado", "lead", "principal"],
        "Semi-Senior": ["semi senior", "intermedio", "mid-level"], 
        "Junior": ["junior", "trainee", "principiante", "entry level"]
    }
    
    # Clusters de skills (skills que suelen aparecer juntas)
    skill_clusters = identificar_clusters_skills(df)
    classification_results["skill_clusters"] = skill_clusters
    
    # Tendencias del mercado
    trends = analizar_tendencias(df)
    classification_results["market_trends"] = trends
    
    print("✅ Clasificación avanzada completada")
    return classification_results

def identificar_clusters_skills(df: pd.DataFrame) -> Dict:
    """
    Identifica clusters de skills que suelen aparecer juntas
    """
    # Clusters predefinidos basados en roles
    clusters = {
        "Business Analyst": {
            "skills": ["SQL", "Power BI", "Excel", "Business Intelligence", "Análisis de Datos"],
            "descripcion": "Análisis de negocio y datos"
        },
        "Consultor ERP": {
            "skills": ["SAP", "Oracle", "ERP", "Gestión de Procesos"],
            "descripcion": "Implementación sistemas empresariales"
        },
        "Data Scientist": {
            "skills": ["Python", "Machine Learning", "SQL", "Data Analysis"],
            "descripcion": "Ciencia de datos y machine learning"
        },
        "Project Manager": {
            "skills": ["Project Management", "Scrum", "Agile", "Liderazgo"],
            "descripcion": "Gestión de proyectos y equipos"
        },
        "Control de Gestión": {
            "skills": ["Control de Gestión", "KPI", "Dashboard", "Presupuesto", "Análisis Financiero"],
            "descripcion": "Control y análisis de gestión empresarial"
        }
    }
    
    # Calcular fuerza de cada cluster basado en frecuencia de skills
    cluster_strength = {}
    for cluster_name, cluster_data in clusters.items():
        strength = 0
        skills_encontradas = []
        
        for skill in cluster_data["skills"]:
            if skill in df['skill'].values:
                skill_freq = df[df['skill'] == skill]['frecuencia'].iloc[0]
                strength += skill_freq
                skills_encontradas.append(skill)
        
        if skills_encontradas:
            cluster_strength[cluster_name] = {
                "strength": strength,
                "skills_encontradas": skills_encontradas,
                "cobertura": len(skills_encontradas) / len(cluster_data["skills"]),
                "descripcion": cluster_data["descripcion"]
            }
    
    return cluster_strength

def analizar_tendencias(df: pd.DataFrame) -> Dict:
    """
    Analiza tendencias del mercado basado en frecuencia de skills
    """
    # Consideramos "emergentes" skills con alta frecuencia relativa
    total_ofertas = df['frecuencia'].sum()
    
    tendencias = {
        "skills_explosivas": [],
        "skills_estables": [], 
        "skills_declinando": [],
        "hot_skills": []
    }
    
    for _, row in df.iterrows():
        skill = row['skill']
        frecuencia = row['frecuencia']
        porcentaje = row['porcentaje']
        
        # Skills explosivas (alta frecuencia relativa)
        if porcentaje > 15:
            tendencias["skills_explosivas"].append({
                "skill": skill,
                "porcentaje": porcentaje,
                "categoria": "Alta Demanda"
            })
        
        # Hot skills (entre 5% y 15%)
        elif porcentaje > 5:
            tendencias["hot_skills"].append({
                "skill": skill, 
                "porcentaje": porcentaje,
                "categoria": "Demanda Media"
            })
        
        # Skills estables (entre 1% y 5%)
        elif porcentaje > 1:
            tendencias["skills_estables"].append({
                "skill": skill,
                "porcentaje": porcentaje, 
                "categoria": "Demanda Estable"
            })
    
    # Ordenar por porcentaje
    for categoria in tendencias:
        tendencias[categoria] = sorted(tendencias[categoria], 
                                     key=lambda x: x['porcentaje'], reverse=True)[:5]
    
    return tendencias

def generar_matriz_competencias(df: pd.DataFrame, usuario_skills: List[str]) -> pd.DataFrame:
    """
    Genera matriz de competencias usuario vs mercado
    """
    matriz_data = []
    
    for _, row in df.iterrows():
        skill_mercado = row['skill']
        frecuencia = row['frecuencia']
        porcentaje = row['porcentaje']
        
        # Verificar si usuario tiene la skill
        usuario_tiene = skill_mercado in usuario_skills
        
        # Calificar importancia
        if porcentaje > 10:
            importancia = "Crítica"
        elif porcentaje > 5:
            importancia = "Alta"
        elif porcentaje > 2:
            importancia = "Media"
        else:
            importancia = "Baja"
        
        # Recomendación
        if usuario_tiene and importancia in ["Crítica", "Alta"]:
            recomendacion = "Mantener y profundizar"
        elif not usuario_tiene and importancia in ["Crítica", "Alta"]:
            recomendacion = "Aprender urgentemente"
        elif not usuario_tiene and importancia == "Media":
            recomendacion = "Aprender pronto"
        else:
            recomendacion = "Opcional"
        
        matriz_data.append({
            'skill': skill_mercado,
            'frecuencia_mercado': frecuencia,
            'porcentaje_mercado': porcentaje,
            'usuario_tiene': usuario_tiene,
            'importancia': importancia,
            'recomendacion': recomendacion
        })
    
    return pd.DataFrame(matriz_data)

