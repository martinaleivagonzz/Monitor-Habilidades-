# etl/transform.py
# -*- coding: utf-8 -*-
import pandas as pd
import re
from typing import List, Dict

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa los datos crudos y extrae skills de las descripciones
    """
    print("🔹 Transformando datos y extrayendo skills...")
    
    # Asegurar que existen las columnas esenciales
    if 'company' not in df.columns:
        df['company'] = "No especificada"
    
    if 'location' not in df.columns:
        df['location'] = "Chile"
    
    if 'experience_text' not in df.columns:
        df['experience_text'] = ""
    
    # 1. Limpiar descripciones
    df['descripcion_limpia'] = df['descripcion'].apply(clean_description)
    
    # 2. Extraer skills técnicas
    df['skills_tecnicas'] = df['descripcion_limpia'].apply(extract_technical_skills)
    
    # 3. Extraer skills de gestión
    df['skills_gestion'] = df['descripcion_limpia'].apply(extract_management_skills)
    
    # 4. Extraer nivel de experiencia
    df['nivel_experiencia'] = df['descripcion_limpia'].apply(extract_experience_level)
    
    # 5. Categorizar el trabajo
    df['categoria'] = df.apply(categorize_job, axis=1)
    
    print(f"✅ Skills extraídas de {len(df)} descripciones")
    return df

def clean_description(text: str) -> str:
    """Limpia el texto de la descripción"""
    if pd.isna(text):
        return ""
    
    # Convertir a minúsculas y limpiar
    text = str(text).lower()
    text = re.sub(r'<[^>]+>', '', text)  # Remover HTML
    text = re.sub(r'\s+', ' ', text)     # Remover espacios múltiples
    text = re.sub(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', ' ', text)  # Remover caracteres especiales
    return text.strip()

def extract_technical_skills(descripcion: str) -> List[str]:
    """Extrae skills técnicas para Control de Gestión + TI"""
    skills_found = []
    desc_lower = str(descripcion).lower()
    
    # SKILLS TÉCNICAS CLAVE
    technical_skills = {
        # ERP Systems (alto valor)
        'SAP': ['sap', 'sap fi', 'sap co', 'sap sd', 'sap pp', 'sap hana', 'sap erp'],
        'Oracle': ['oracle', 'oracle erp', 'oracle fusion'],
        'ERP': ['erp', 'enterprise resource planning'],
        'Microsoft Dynamics': ['microsoft dynamics', 'dynamics 365'],
        
        # Business Intelligence (alto valor)
        'Power BI': ['power bi', 'powerbi'],
        'Tableau': ['tableau'],
        'Qlik': ['qlik', 'qlikview', 'qlik sense'],
        'Business Intelligence': ['business intelligence', 'bi', 'inteligencia de negocios'],
        
        # Bases de Datos
        'SQL': ['sql', 'mysql', 'postgresql', 'sql server', 'oracle database'],
        'Excel': ['excel', 'excel avanzado', 'macro excel'],
        'Python': ['python', 'pandas', 'numpy', 'scikit-learn'],
        'R': ['r ', 'r programming', 'r studio'],
        
        # Gestión de Procesos
        'BPMN': ['bpmn', 'business process model'],
        'Process Mining': ['process mining', 'minería de procesos'],
        
        # Metodologías
        'Scrum': ['scrum', 'scrum master'],
        'Agile': ['ágil', 'agile', 'metodologías ágiles'],
        'Kanban': ['kanban'],
        'Waterfall': ['waterfall', 'cascada'],
        
        # Cloud & Herramientas
        'GCP': ['gcp', 'google cloud', 'bigquery'],
        'AWS': ['aws', 'amazon web services'],
        'Azure': ['azure', 'microsoft azure']
    }
    
    for skill_group, keywords in technical_skills.items():
        for keyword in keywords:
            if keyword in desc_lower:
                skills_found.append(skill_group)
                break  # Evitar duplicados dentro del mismo grupo
    
    return list(set(skills_found))  # Eliminar duplicados

def extract_management_skills(descripcion: str) -> List[str]:
    """Extrae skills de gestión"""
    skills_found = []
    desc_lower = str(descripcion).lower()
    
    management_skills = {
        # Gestión de Proyectos
        'Project Management': ['project management', 'gestión de proyectos', 'gerente de proyecto'],
        'PMP': ['pmp', 'project management professional'],
        'PMBOK': ['pmbok'],
        
        # Control de Gestión
        'Control de Gestión': ['control de gestión', 'control gestion'],
        'KPI': ['kpi', 'indicadores', 'métricas', 'key performance indicator'],
        'Dashboard': ['dashboard', 'cuadro de mando'],
        'Presupuesto': ['presupuesto', 'budget', 'forecast', 'control presupuestario'],
        'Análisis Financiero': ['análisis financiero', 'financial analysis'],
        
        # Análisis de Negocio
        'Business Analysis': ['business analysis', 'análisis de negocio'],
        'Requerimientos': ['requerimientos', 'requirements', 'requisitos'],
        'Stakeholder Management': ['stakeholder', 'gestión de stakeholders'],
        'Change Management': ['change management', 'gestión del cambio'],
        
        # Mejora Continua
        'Lean': ['lean', 'lean manufacturing'],
        'Six Sigma': ['six sigma'],
        'Mejora Continua': ['mejora continua', 'continuous improvement'],
        'Transformación Digital': ['transformación digital', 'digital transformation'],
        
        # Analytics
        'Data Analysis': ['data analysis', 'análisis de datos'],
        'Market Insights': ['market insights', 'consumer insights'],
        'Business Analytics': ['business analytics']
    }
    
    for skill_group, keywords in management_skills.items():
        for keyword in keywords:
            if keyword in desc_lower:
                skills_found.append(skill_group)
                break
    
    return list(set(skills_found))

def extract_experience_level(descripcion: str) -> str:
    """Extrae el nivel de experiencia requerido"""
    desc_lower = str(descripcion).lower()
    
    senior_keywords = ['senior', 'sr.', 'experto', 'avanzado', 'lead', 'principal', '+5 años', '5+ años']
    semi_senior_keywords = ['semi senior', 'semi-senior', 'intermedio', 'mid-level', '3 años', '3+ años', '2-4 años']
    junior_keywords = ['junior', 'jr.', 'trainee', 'principiante', 'entry level', '0-2 años', 'reciente egreso']
    
    if any(word in desc_lower for word in senior_keywords):
        return 'Senior'
    elif any(word in desc_lower for word in semi_senior_keywords):
        return 'Semi-Senior'
    elif any(word in desc_lower for word in junior_keywords):
        return 'Junior'
    else:
        return 'No especificado'

def categorize_job(row):
    """Categoriza el trabajo para análisis"""
    title = str(row['title']).lower()
    skills_tecnicas = row['skills_tecnicas']
    skills_gestion = row['skills_gestion']
    
    all_skills = skills_tecnicas + skills_gestion
    
    # Prioridad de categorías
    if any(skill in all_skills for skill in ['SAP', 'Oracle', 'ERP']):
        return 'Consultor ERP'
    elif any(skill in all_skills for skill in ['Power BI', 'Tableau', 'Business Intelligence']):
        return 'Business Intelligence'
    elif any(skill in all_skills for skill in ['Project Management', 'PMP']):
        return 'Gestión de Proyectos'
    elif any(skill in all_skills for skill in ['Control de Gestión', 'KPI', 'Presupuesto']):
        return 'Control de Gestión'
    elif 'business analyst' in title or 'business analysis' in all_skills:
        return 'Business Analyst'
    elif 'data' in title and any(skill in all_skills for skill in ['Python', 'SQL', 'Data Analysis']):
        return 'Data Analyst'
    else:
        return 'Otros'

def analyze_skills_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza la frecuencia de skills y crea resumen
    """
    print("📊 Analizando frecuencia de skills...")
    
    # Combinar todas las skills
    all_skills = []
    for _, row in df.iterrows():
        all_skills.extend(row['skills_tecnicas'])
        all_skills.extend(row['skills_gestion'])
    
    # Contar frecuencia
    skills_count = pd.Series(all_skills).value_counts().reset_index()
    skills_count.columns = ['skill', 'frecuencia']
    
    # Calcular porcentaje
    total_ofertas = len(df)
    skills_count['porcentaje'] = (skills_count['frecuencia'] / total_ofertas * 100).round(2)
    
    # Ordenar por frecuencia
    skills_count = skills_count.sort_values('frecuencia', ascending=False)
    
    print(f"✅ {len(skills_count)} skills únicas identificadas")
    return skills_count

def analyze_skills_by_seniority(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza skills por nivel de experiencia
    """
    print("🎯 Analizando skills por seniority...")
    
    # Expandir skills para análisis
    skills_data = []
    
    for _, row in df.iterrows():
        nivel = row['nivel_experiencia']
        for skill in row['skills_tecnicas'] + row['skills_gestion']:
            skills_data.append({
                'skill': skill,
                'nivel_experiencia': nivel,
                'categoria': row['categoria']
            })
    
    if skills_data:
        skills_df = pd.DataFrame(skills_data)
        
        # Agrupar por skill y nivel
        skills_by_level = skills_df.groupby(['skill', 'nivel_experiencia']).size().reset_index()
        skills_by_level.columns = ['skill', 'nivel_experiencia', 'frecuencia']
        
        # Ordenar
        skills_by_level = skills_by_level.sort_values(['skill', 'frecuencia'], ascending=[True, False])
        
        print(f"✅ Skills analizadas por nivel de experiencia")
        return skills_by_level
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # Para testing
    sample_data = {
        'title': ['Business Analyst SAP', 'Data Analyst Python'],
        'company': ['Empresa A', 'Empresa B'],
        'location': ['Santiago', 'Remote'],
        'descripcion': [
            'Se busca business analyst con experiencia en SAP FI y Power BI',
            'Data analyst con Python, SQL y machine learning para análisis de datos'
        ]
    }
    
    df_test = pd.DataFrame(sample_data)
    df_processed = transform_data(df_test)
    
    print("\n🧪 TEST RESULTADOS:")
    print(df_processed[['title', 'skills_tecnicas', 'skills_gestion', 'nivel_experiencia', 'categoria']])
    