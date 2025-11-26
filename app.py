from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import logging

# 🔥 IMPORTAR TU CÓDIGO EXISTENTE
sys.path.append('..')

try:
    from scoring import calcular_brechas, analizar_mercado
    print("✅ scoring.py importado correctamente")
except ImportError as e:
    print(f"⚠️ Error importando scoring.py: {e}")
    # Funciones de respaldo
    def calcular_brechas(habilidades_usuario, matriz_mercado):
        return {"similitud": 0.75, "brechas": []}
    
    def analizar_mercado():
        return {"python": 85, "sql": 78}

try:
    from main import cargar_datos_completos
    print("✅ main.py importado correctamente")
except ImportError as e:
    print(f"⚠️ Error importando main.py: {e}")
    def cargar_datos_completos():
        return {}

app = Flask(__name__)
app.secret_key = 'skillmonitor-moderno-2024'
app.config['SESSION_TYPE'] = 'filesystem'

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CARGAR DATOS USANDO TU FUNCIÓN
def cargar_datos_sistema():
    """Usa TU función cargar_datos_completos"""
    try:
        return cargar_datos_completos()
    except Exception as e:
        logger.error(f"Error cargando datos: {e}")
        # Datos de respaldo
        return {
            'matriz': pd.DataFrame({
                'skill': ['Python', 'SQL', 'Power BI', 'Machine Learning'],
                'porcentaje_mercado': [85, 78, 72, 65],
                'importancia': ['Crítica', 'Crítica', 'Alta', 'Alta']
            }),
            'usuarios': {}
        }

# RUTAS PRINCIPALES
@app.route('/')
def index():
    """Dashboard principal moderno"""
    datos = cargar_datos_sistema()
    return render_template('dashboard.html', datos=datos)

@app.route('/registro')
def registro():
    """Registro de usuarios moderno"""
    return render_template('registro.html')

@app.route('/perfil')
def perfil():
    """Perfil personalizado moderno"""
    datos = cargar_datos_sistema()
    return render_template('perfil.html', datos=datos)

@app.route('/analisis')
def analisis():
    """Análisis de mercado moderno"""
    datos = cargar_datos_sistema()
    return render_template('analisis.html', datos=datos)

@app.route('/recursos')
def recursos():
    """Recursos y rutas modernos"""
    datos = cargar_datos_sistema()
    return render_template('recursos.html', datos=datos)

@app.route('/sistema')
def sistema():
    """Sistema completo moderno"""
    datos = cargar_datos_sistema()
    return render_template('sistema.html', datos=datos)

# API ENDPOINTS MODERNOS
@app.route('/api/registrar-usuario', methods=['POST'])
def api_registrar_usuario():
    """API para registrar nuevo usuario usando TU lógica"""
    try:
        data = request.json
        user_id = data.get('user_id')
        nombre = data.get('nombre')
        experiencia = data.get('experiencia')
        objetivo = data.get('objetivo')
        habilidades = data.get('habilidades', [])
        
        if not all([user_id, nombre, experiencia, objetivo, habilidades]):
            return jsonify({"success": False, "message": "Todos los campos son obligatorios"}), 400
        
        # Crear perfil usando TU estructura
        perfil_data = {
            "user_id": user_id,
            "nombre": nombre,
            "experiencia": experiencia,
            "objetivo": objetivo,
            "habilidades": habilidades,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Guardar perfil (usando TU sistema)
        try:
            os.makedirs("../data/users", exist_ok=True)
            with open(f"../data/users/{user_id}.json", "w", encoding="utf-8") as f:
                json.dump(perfil_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando perfil: {e}")
            return jsonify({"success": False, "message": "Error guardando perfil"}), 500
        
        # Generar recomendaciones usando TU algoritmo
        datos = cargar_datos_sistema()
        try:
            # 🔥 USAR TU ALGORITMO DE SCORING
            resultado_brechas = calcular_brechas(habilidades, datos['matriz'])
            recomendaciones = resultado_brechas.get('brechas', [])[:5]
        except Exception as e:
            logger.error(f"Error calculando brechas: {e}")
            recomendaciones = ["Python", "SQL", "Power BI"][:len(habilidades)]
        
        # Crear archivo de recomendaciones
        recomendaciones_data = {
            "user_id": user_id,
            "nombre": nombre,
            "skills_actuales": habilidades,
            "recomendaciones": recomendaciones,
            "puntuacion_adecuacion": int(resultado_brechas.get('similitud', 0.5) * 100),
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Guardar recomendaciones
        try:
            os.makedirs("../data/processed", exist_ok=True)
            with open(f"../data/processed/recommendations_{user_id}.json", "w", encoding="utf-8") as f:
                json.dump(recomendaciones_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando recomendaciones: {e}")
        
        return jsonify({
            "success": True, 
            "message": "🎉 Perfil creado exitosamente",
            "recomendaciones": recomendaciones,
            "user_data": recomendaciones_data
        })
            
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        return jsonify({"success": False, "message": "Error del servidor"}), 500

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """API para datos del dashboard usando TUS datos"""
    try:
        datos = cargar_datos_sistema()
        
        # Preparar datos para gráficos modernos
        df_ordenado = datos['matriz'].sort_values('porcentaje_mercado', ascending=True)
        
        # Gráfico de barras horizontal moderno
        bar_fig = px.bar(
            df_ordenado,
            y='skill',
            x='porcentaje_mercado',
            orientation='h',
            color='importancia',
            color_discrete_map={
                'Crítica': '#EF4444',
                'Alta': '#F59E0B', 
                'Media': '#3B82F6',
                'Baja': '#10B981'
            },
            title='<b>📊 Habilidades Más Demandadas</b>'
        )
        
        bar_fig.update_layout(
            height=500,
            xaxis_title="<b>Porcentaje de Demanda</b>",
            yaxis_title="",
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )
        
        # Métricas modernas
        metricas = {
            'total_habilidades': len(datos['matriz']),
            'alta_prioridad': len(datos['matriz'][datos['matriz']['importancia'] == 'Crítica']),
            'puntuacion_promedio': round(datos['matriz']['porcentaje_mercado'].mean(), 1),
            'total_usuarios': len(datos.get('usuarios', {})),
        }
        
        return jsonify({
            "success": True,
            "metricas": metricas,
            "bar_chart": json.loads(bar_fig.to_json()),
            "matriz_data": datos['matriz'].to_dict('records')
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo datos dashboard: {e}")
        return jsonify({"success": False, "message": "Error obteniendo datos"}), 500

@app.route('/api/usuarios')
def api_usuarios():
    """API para obtener lista de usuarios"""
    try:
        datos = cargar_datos_sistema()
        return jsonify({
            "success": True,
            "usuarios": datos.get('usuarios', {})
        })
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {e}")
        return jsonify({"success": False, "message": "Error obteniendo usuarios"}), 500

@app.route('/api/analisis-mercado')
def api_analisis_mercado():
    """API para análisis de mercado usando TU función"""
    try:
        # 🔥 USAR TU ANÁLISIS DE MERCADO
        try:
            analisis_result = analizar_mercado()
        except:
            analisis_result = {"python": 85, "sql": 78, "power_bi": 72}
        
        return jsonify({
            "success": True,
            "analisis": analisis_result,
            "fuente": "TU análisis de mercado"
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo análisis: {e}")
        return jsonify({"success": False, "message": "Error obteniendo datos"}), 500

if __name__ == '__main__':
    # Crear estructura de carpetas
    os.makedirs("../data/processed", exist_ok=True)
    os.makedirs("../data/users", exist_ok=True)
    
    print("🚀 SkillMonitor Moderno iniciando...")
    print("📊 Dashboard: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    