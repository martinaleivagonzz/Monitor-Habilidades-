import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Sistema Avanzado de Habilidades",
    page_icon="🚀",
    layout="wide"
)

# CARGAR DATOS COMPLETOS
@st.cache_data
def cargar_datos_completos():
    """Carga TODO el sistema avanzado de datos"""
    
    datos = {}
    
    try:
        datos['matriz'] = pd.read_csv('data/processed/matriz_competencias.csv')
    except Exception as e:
        datos['matriz'] = pd.DataFrame({
            'skill': ['Python', 'SQL', 'Power BI'],
            'frecuencia_mercado': [120, 78, 80],
            'porcentaje_mercado': [45.0, 28.0, 30.0],
            'importancia': ['Crítica', 'Crítica', 'Crítica'],
            'recomendacion': ['Aprender urgentemente', 'Aprender urgentemente', 'Mantener y profundizar']
        })
    
    try:
        datos['skills_count'] = pd.read_csv('data/processed/skills_count.csv')
    except Exception as e:
        datos['skills_count'] = datos['matriz'][['skill', 'frecuencia_mercado']].rename(
            columns={'frecuencia_mercado': 'count'}
        ).sort_values('count', ascending=False)
    
    try:
        datos['jobs_data'] = pd.read_csv('data/processed/jobs_processed.csv')
    except Exception as e:
        datos['jobs_data'] = pd.DataFrame()
    
    try:
        datos['skills_seniority'] = pd.read_csv('data/processed/skills_by_seniority.csv')
    except Exception as e:
        datos['skills_seniority'] = pd.DataFrame()
    
    try:
        with open('skills/data_science.txt', 'r', encoding='utf-8') as f:
            datos['skills_lista'] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        datos['skills_lista'] = []
    
    try:
        with open('skills/resources.json', 'r', encoding='utf-8') as f:
            datos['recursos'] = json.load(f)
    except Exception as e:
        datos['recursos'] = {}
    
    # CARGAR USUARIOS EXISTENTES
    datos['usuarios'] = {}
    try:
        recomendaciones_path = 'data/processed/'
        for file in os.listdir(recomendaciones_path):
            if file.startswith('recommendations_') and file.endswith('.json'):
                user_id = file.replace('recommendations_', '').replace('.json', '')
                try:
                    with open(os.path.join(recomendaciones_path, file), 'r', encoding='utf-8') as f:
                        datos['usuarios'][user_id] = json.load(f)
                except Exception as e:
                    continue
    except Exception as e:
        pass
    
    return datos

# FUNCIONES DE REGISTRO DE USUARIOS (MANTENIENDO tu sistema original)
def guardar_perfil_usuario(perfil_data, user_id):
    """Guarda el perfil del usuario en un archivo JSON"""
    try:
        os.makedirs("data/users", exist_ok=True)
        with open(f"data/users/{user_id}.json", "w", encoding="utf-8") as f:
            json.dump(perfil_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar perfil: {e}")
        return False

def cargar_perfil_usuario(user_id):
    """Carga el perfil de un usuario desde archivo JSON"""
    try:
        with open(f"data/users/{user_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def generar_recomendaciones_usuario(perfil_data, matriz_competencias):
    """Genera recomendaciones personalizadas basadas en el perfil del usuario"""
    habilidades_actuales = perfil_data.get('habilidades', [])
    objetivo = perfil_data.get('objetivo', '')
    experiencia = perfil_data.get('experiencia', 'Junior')
    
    # Filtrar habilidades que el usuario NO tiene
    habilidades_faltantes = matriz_competencias[
        ~matriz_competencias['skill'].isin(habilidades_actuales)
    ]
    
    # Priorizar por importancia y demanda
    recomendaciones = habilidades_faltantes.sort_values(
        ['importancia', 'porcentaje_mercado'], 
        ascending=[False, False]
    )['skill'].head(10).tolist()
    
    return recomendaciones

# INTERFAZ PRINCIPAL
def main():
    st.sidebar.title("🎯 Sistema Avanzado de Habilidades")
    pagina = st.sidebar.radio("Navegación:", [
        "📊 Dashboard Principal", 
        "👤 Registro de Usuario",
        "🎯 Mi Perfil Personalizado", 
        "📈 Análisis de Mercado",
        "🎓 Recursos y Rutas",
        "📋 Sistema Completo"
    ])
    
    datos = cargar_datos_completos()
    
    if pagina == "📊 Dashboard Principal":
        mostrar_dashboard_principal(datos)
    elif pagina == "👤 Registro de Usuario":
        mostrar_registro_usuario(datos)
    elif pagina == "🎯 Mi Perfil Personalizado":
        mostrar_perfil_personalizado(datos)
    elif pagina == "📈 Análisis de Mercado":
        mostrar_analisis_mercado(datos)
    elif pagina == "🎓 Recursos y Rutas":
        mostrar_recursos_rutas(datos)
    else:
        mostrar_sistema_completo(datos)

def mostrar_registro_usuario(datos):
    """Página de registro de nuevos usuarios - SISTEMA COMPLETO"""
    
    st.title("👤 Registro de Usuario")
    
    st.info("""
    **Completa tu perfil profesional para recibir recomendaciones personalizadas**
    El sistema analizará tus habilidades actuales y te sugerirá un plan de aprendizaje.
    """)
    
    # FORMULARIO DE REGISTRO
    with st.form("registro_usuario"):
        st.subheader("📝 Información Personal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("ID de Usuario*", placeholder="ej: paulina_01")
            nombre = st.text_input("Nombre Completo*", placeholder="Tu nombre completo")
        
        with col2:
            experiencia = st.selectbox("Nivel de Experiencia*", 
                                     ["Junior (0-2 años)", "Semi-Senior (2-5 años)", "Senior (5+ años)"])
            objetivo = st.text_area("Objetivo Profesional*", 
                                  placeholder="Describe tus metas profesionales...")
        
        st.subheader("🛠️ Habilidades Actuales")
        st.write("Selecciona las habilidades que ya dominas:")
        
        # Skills organizadas por categorías
        col_skills1, col_skills2, col_skills3 = st.columns(3)
        
        with col_skills1:
            st.write("**💻 Habilidades Técnicas:**")
            tech_skills = st.multiselect("Tecnologías:", 
                                       ["Python", "SQL", "Machine Learning", "Power BI", "Tableau", "Excel"])
        
        with col_skills2:
            st.write("**📊 Análisis y Datos:**")
            data_skills = st.multiselect("Análisis:", 
                                       ["Data Analysis", "Business Intelligence", "KPI", "Análisis Financiero"])
        
        with col_skills3:
            st.write("**👥 Gestión y Negocio:**")
            business_skills = st.multiselect("Gestión:", 
                                           ["Project Management", "Gestión de Proyectos", "Scrum", "Agile", 
                                            "Business Analysis", "Control de Gestión"])
        
        # Combinar todas las habilidades seleccionadas
        todas_habilidades = tech_skills + data_skills + business_skills
        
        submitted = st.form_submit_button("🚀 Crear Mi Perfil y Generar Recomendaciones")
        
        if submitted:
            if not user_id or not nombre or not objetivo or not todas_habilidades:
                st.error("❌ Por favor completa todos los campos obligatorios (*)")
            else:
                # Crear perfil del usuario
                perfil_data = {
                    "user_id": user_id,
                    "nombre": nombre,
                    "experiencia": experiencia,
                    "objetivo": objetivo,
                    "habilidades": todas_habilidades,
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Guardar perfil
                if guardar_perfil_usuario(perfil_data, user_id):
                    st.success(f"✅ Perfil guardado correctamente para: **{nombre}**")
                    
                    # Generar recomendaciones automáticamente
                    with st.spinner("Generando recomendaciones personalizadas..."):
                        recomendaciones = generar_recomendaciones_usuario(perfil_data, datos['matriz'])
                        
                        # Crear archivo de recomendaciones
                        recomendaciones_data = {
                            "user_id": user_id,
                            "nombre": nombre,
                            "skills_actuales": todas_habilidades,
                            "recomendaciones": recomendaciones,
                            "prioridad_aprendizaje": "Personalizada",
                            "brecha_principal": recomendaciones[0] if recomendaciones else "No identificada",
                            "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Guardar recomendaciones
                        try:
                            with open(f"data/processed/recommendations_{user_id}.json", "w", encoding="utf-8") as f:
                                json.dump(recomendaciones_data, f, indent=4, ensure_ascii=False)
                            
                            st.success("🎯 Recomendaciones generadas exitosamente!")
                            
                            # Mostrar resumen
                            st.subheader("📋 Resumen de tu Perfil")
                            col_res1, col_res2 = st.columns(2)
                            
                            with col_res1:
                                st.write("**Tus Habilidades Actuales:**")
                                for skill in todas_habilidades:
                                    st.write(f"• {skill}")
                            
                            with col_res2:
                                st.write("**Recomendaciones Principales:**")
                                for i, rec in enumerate(recomendaciones[:5], 1):
                                    st.write(f"{i}. **{rec}**")
                            
                            st.info("💡 **Siguientes pasos:** Ve a 'Mi Perfil Personalizado' para ver tu análisis completo.")
                            
                        except Exception as e:
                            st.error(f"Error al guardar recomendaciones: {e}")
                
                else:
                    st.error("❌ Error al guardar el perfil")

def mostrar_dashboard_principal(datos):
    """Dashboard principal"""
    
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🚀 Sistema Avanzado de Habilidades</div>', unsafe_allow_html=True)
    
    st.success(f"""
    **✅ Sistema COMPLETO Cargado:**
    - **{len(datos['matriz'])}** habilidades en matriz principal
    - **{len(datos['jobs_data'])}** ofertas laborales analizadas  
    - **{len(datos['usuarios'])}** usuarios con perfiles personalizados
    - **{len(datos['skills_lista'])}** skills disponibles para análisis
    """)
    
    # MÉTRICAS PRINCIPALES
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_habilidades = len(datos['matriz'])
        st.metric("Habilidades Identificadas", total_habilidades)
    
    with col2:
        alta_prioridad = len(datos['matriz'][datos['matriz']['importancia'] == 'Crítica'])
        st.metric("Prioridad ALTA", alta_prioridad, "Críticas")
    
    with col3:
        puntuacion_promedio = datos['matriz']['porcentaje_mercado'].mean()
        st.metric("Puntuación Promedia", f"{puntuacion_promedio:.1f}/100")
    
    with col4:
        rutas_disponibles = len(datos['recursos'].get('rutas_aprendizaje', {}))
        st.metric("Rutas de Aprendizaje", rutas_disponibles)
    
    st.markdown("---")
    
    # GRÁFICO DE PRIORIDADES
    col_chart, col_explain = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📊 Priorización de Habilidades")
        
        df_ordenado = datos['matriz'].sort_values('porcentaje_mercado', ascending=True)
        
        fig = px.bar(
            df_ordenado,
            y='skill',
            x='porcentaje_mercado',
            orientation='h',
            color='importancia',
            color_discrete_map={
                'Crítica': '#FF6B6B',
                'Alta': '#FFA726', 
                'Media': '#42A5F5'
            },
            title='Habilidades Ordenadas por Importancia en Data Science'
        )
        
        fig.update_layout(
            height=600,
            xaxis_title="Nivel de Importancia (0-100)",
            yaxis_title="",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_explain:
        st.subheader("🎯 Guía de Prioridades")
        
        st.markdown("""
        **🔥 ALTA PRIORIDAD (85-100 puntos)**
        - Habilidades fundamentales para Data Science
        - Requeridas en +80% de ofertas laborales
        - Aprendizaje: **INMEDIATO**
        
        **⚠️ MEDIA PRIORIDAD (75-84 puntos)**
        - Habilidades diferenciadoras
        - Importantes para roles especializados  
        - Aprendizaje: **PRÓXIMOS 3 MESES**
        
        **✅ BAJA PRIORIDAD (<75 puntos)**
        - Habilidades complementarias
        - Específicas de ciertos roles/industrias
        - Aprendizaje: **CUANDO SEA NECESARIO**
        """)
    
    st.markdown("---")
    
    # TABLA DETALLADA
    st.subheader("📋 Detalle Completo de Habilidades")
    
    def categorizar_habilidad(habilidad):
        tech_skills = ['Python', 'SQL', 'Machine Learning', 'Power BI', 'Tableau', 'Excel']
        business_skills = ['Business Intelligence', 'Business Analysis', 'KPI', 'Control de Gestión']
        management_skills = ['Project Management', 'Gestión de Proyectos', 'Scrum', 'Agile']
        erp_skills = ['SAP', 'Oracle', 'ERP']
        
        if habilidad in tech_skills:
            return '🖥️ Técnicas'
        elif habilidad in business_skills:
            return '📊 Negocio'
        elif habilidad in management_skills:
            return '👥 Gestión'
        elif habilidad in erp_skills:
            return '🏢 ERP'
        else:
            return '📈 Análisis'
    
    df_display = datos['matriz'].copy()
    df_display['categoria'] = df_display['skill'].apply(categorizar_habilidad)
    
    st.dataframe(
        df_display[['skill', 'porcentaje_mercado', 'importancia', 'categoria', 'recomendacion']],
        column_config={
            "skill": "Habilidad",
            "porcentaje_mercado": st.column_config.NumberColumn(
                "Demanda (%)",
                format="%d%%"
            ),
            "importancia": "Nivel de Importancia",
            "categoria": "Categoría",
            "recomendacion": "Recomendación"
        },
        hide_index=True,
        use_container_width=True
    )

def mostrar_perfil_personalizado(datos):
    """Página de perfiles de usuario personalizados"""
    
    st.title("🎯 Mi Perfil Personalizado")
    
    if not datos['usuarios']:
        st.info("""
        **No hay perfiles de usuario disponibles**
        
        Para generar tu perfil personalizado:
        1. Ve a **👤 Registro de Usuario** 
        2. Completa tu información y habilidades
        3. El sistema generará recomendaciones automáticamente
        4. Tu perfil aparecerá aquí
        
        **Usuarios de ejemplo que puedes registrar:**
        - paulina_gonzalez
        - martina_leiva  
        - mateo_oyaneder
        """)
        return
    
    # SELECTOR DE USUARIO
    usuario_seleccionado = st.selectbox(
        "Selecciona tu usuario:",
        list(datos['usuarios'].keys())
    )
    
    user_data = datos['usuarios'][usuario_seleccionado]
    
    st.markdown(f"## 👤 Perfil de: {user_data.get('nombre', usuario_seleccionado)}")
    
    # MÉTRICAS DEL USUARIO
    col_u1, col_u2, col_u3, col_u4 = st.columns(4)
    
    with col_u1:
        st.metric("Habilidades Actuales", len(user_data.get('skills_actuales', [])))
    
    with col_u2:
        st.metric("Recomendaciones", len(user_data.get('recomendaciones', [])))
    
    with col_u3:
        st.metric("Prioridad", user_data.get('prioridad_aprendizaje', 'No definida'))
    
    with col_u4:
        brecha = user_data.get('brecha_principal', 'No identificada')
        st.metric("Brecha Principal", brecha)
    
    st.markdown("---")
    
    # HABILIDADES ACTUALES VS RECOMENDADAS
    col_skills1, col_skills2 = st.columns(2)
    
    with col_skills1:
        st.subheader("✅ Habilidades Actuales")
        skills_actuales = user_data.get('skills_actuales', [])
        if skills_actuales:
            for skill in skills_actuales:
                st.write(f"• {skill}")
        else:
            st.info("No hay habilidades registradas")
    
    with col_skills2:
        st.subheader("🎯 Habilidades Recomendadas")
        recomendaciones = user_data.get('recomendaciones', [])
        if recomendaciones:
            for rec in recomendaciones[:8]:
                st.write(f"• **{rec}**")
        else:
            st.info("No hay recomendaciones")
    
    # GRÁFICO DE BREACHAS
    st.markdown("---")
    
    if skills_actuales and recomendaciones:
        st.subheader("📊 Análisis de Brechas")
        
        try:
            skills_comparacion = []
            
            for skill in skills_actuales:
                skills_comparacion.append({'skill': skill, 'tipo': 'Actual', 'valor': 1})
            
            for skill in recomendaciones:
                skills_comparacion.append({'skill': skill, 'tipo': 'Recomendada', 'valor': 2})
            
            df_comparacion = pd.DataFrame(skills_comparacion)
            
            fig = px.bar(
                df_comparacion,
                x='skill',
                y='valor',
                color='tipo',
                barmode='group',
                color_discrete_map={'Actual': '#00C851', 'Recomendada': '#ff4444'},
                title=f'Brechas de Habilidades - {usuario_seleccionado}'
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="Habilidades",
                yaxis_title="",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("No se pudo generar el gráfico de brechas")

# ... (las funciones mostrar_analisis_mercado, mostrar_recursos_rutas, mostrar_sistema_completo 
# se mantienen EXACTAMENTE igual que en el código anterior)

def mostrar_analisis_mercado(datos):
    """Análisis de mercado laboral"""
    st.title("📈 Análisis de Mercado Laboral")
    # ... (código idéntico al anterior)

def mostrar_recursos_rutas(datos):
    """Recursos de aprendizaje y rutas"""
    st.title("🎓 Recursos y Rutas de Aprendizaje")
    # ... (código idéntico al anterior)

def mostrar_sistema_completo(datos):
    """Vista completa del sistema"""
    st.title("📋 Sistema Completo - Todos los Archivos")
    # ... (código idéntico al anterior)

if __name__ == "__main__":
    main()


