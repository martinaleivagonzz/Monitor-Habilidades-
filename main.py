# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
from datetime import datetime

# Importar módulos del proyecto
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.classify import classify_skills_advanced, generar_matriz_competencias
from scoring import calcular_scoring_completo
from profile import menu_seleccionar_usuario, generar_recomendaciones_personalizadas, cargar_perfil_usuario

def main():
    """
    Pipeline ETL completo con sistema multi-usuario
    """
    print("🚀 INICIANDO PIPELINE ETL - MONITOR DE HABILIDADES")
    print("=" * 60)
    
    # PASO 1: EXTRACCIÓN DE DATOS
    print("\n📥 PASO 1: EXTRACCIÓN DE DATOS")
    print("-" * 30)
    
    try:
        df_raw = extract_data()
        if df_raw.empty:
            print("❌ No se pudieron extraer datos. Saliendo...")
            return
        print(f"✅ {len(df_raw)} ofertas extraídas exitosamente")
    except Exception as e:
        print(f"❌ Error en extracción: {e}")
        return
    
    # PASO 2: TRANSFORMACIÓN Y EXTRACCIÓN DE SKILLS
    print("\n🔄 PASO 2: TRANSFORMACIÓN DE DATOS")
    print("-" * 30)
    
    try:
        df_processed = transform_data(df_raw)
        if df_processed.empty:
            print("❌ No se pudieron transformar datos. Saliendo...")
            return
        print(f"✅ {len(df_processed)} ofertas transformadas con skills extraídas")
    except Exception as e:
        print(f"❌ Error en transformación: {e}")
        return
    
    # PASO 3: ANÁLISIS DE FRECUENCIA DE SKILLS
    print("\n📊 PASO 3: ANÁLISIS DE SKILLS")
    print("-" * 30)
    
    try:
        # Combinar todas las skills
        all_skills = []
        for _, row in df_processed.iterrows():
            all_skills.extend(row['skills_tecnicas'])
            all_skills.extend(row['skills_gestion'])
        
        # Contar frecuencia
        skills_count = pd.Series(all_skills).value_counts().reset_index()
        skills_count.columns = ['skill', 'frecuencia']
        
        # Calcular porcentaje
        total_ofertas = len(df_processed)
        skills_count['porcentaje'] = (skills_count['frecuencia'] / total_ofertas * 100).round(2)
        
        # Ordenar
        skills_count = skills_count.sort_values('frecuencia', ascending=False)
        
        print(f"✅ {len(skills_count)} skills únicas identificadas")
        
    except Exception as e:
        print(f"❌ Error en análisis de skills: {e}")
        return
    
    # PASO 4: CLASIFICACIÓN AVANZADA
    print("\n🎯 PASO 4: CLASIFICACIÓN AVANZADA")
    print("-" * 30)
    
    try:
        clasificacion = classify_skills_advanced(skills_count)
        print("✅ Clasificación avanzada completada")
    except Exception as e:
        print(f"❌ Error en clasificación: {e}")
        clasificacion = {}
    
    # PASO 5: SELECCIÓN DE USUARIO
    print("\n" + "=" * 60)
    print("👤 SISTEMA DE RECOMENDACIONES PERSONALIZADAS")
    print("=" * 60)
    
    usuario_id = menu_seleccionar_usuario()
    if not usuario_id:
        print("❌ No se seleccionó usuario. Saliendo...")
        return
    
    # Cargar perfil del usuario
    perfil_usuario = cargar_perfil_usuario(usuario_id)
    if not perfil_usuario:
        print("❌ No se pudo cargar el perfil del usuario. Saliendo...")
        return
    
    print(f"🎯 Usuario seleccionado: {perfil_usuario.get('nombre', usuario_id)}")
    
    # PASO 6: SCORING Y RUTAS DE APRENDIZAJE
    print("\n📈 PASO 6: SCORING PERSONALIZADO")
    print("-" * 30)
    
    try:
        scoring_result = calcular_scoring_completo(skills_count, usuario_id)
        
        if not scoring_result:
            print("❌ No se pudo calcular scoring. Saliendo...")
            return
        
        print("✅ Scoring y rutas de aprendizaje generados")
        
    except Exception as e:
        print(f"❌ Error en scoring: {e}")
        return
    
    # PASO 7: GENERAR RECOMENDACIONES
    print("\n💡 PASO 7: RECOMENDACIONES PERSONALIZADAS")
    print("-" * 30)
    
    try:
        recomendaciones = generar_recomendaciones_personalizadas(usuario_id, skills_count)
        
        if not recomendaciones:
            print("❌ No se pudieron generar recomendaciones")
            return
        
        print("✅ Recomendaciones personalizadas generadas")
        
    except Exception as e:
        print(f"❌ Error en recomendaciones: {e}")
        return
    
    # PASO 8: GUARDAR RESULTADOS
    print("\n💾 PASO 8: GUARDANDO RESULTADOS")
    print("-" * 30)
    
    try:
        # Asegurar que existe la carpeta processed
        os.makedirs("data/processed", exist_ok=True)
        
        # 1. Guardar datos procesados
        df_processed.to_csv("data/processed/jobs_processed.csv", index=False, encoding="utf-8-sig")
        print("✅ jobs_processed.csv guardado")
        
        # 2. Guardar análisis de skills
        skills_count.to_csv("data/processed/skills_count.csv", index=False, encoding="utf-8-sig")
        print("✅ skills_count.csv guardado")
        
        # 3. Guardar scoring
        scoring_result['scoring_df'].to_csv("data/processed/scoring_skills.csv", index=False, encoding="utf-8-sig")
        print("✅ scoring_skills.csv guardado")
        
        # 4. Guardar matriz de competencias
        scoring_result['matriz_competencias'].to_csv("data/processed/matriz_competencias.csv", index=False, encoding="utf-8-sig")
        print("✅ matriz_competencias.csv guardado")
        
        # 5. Guardar clasificación avanzada
        with open("data/processed/clasificacion_avanzada.json", "w", encoding="utf-8") as f:
            json.dump(scoring_result['clasificacion_avanzada'], f, indent=2, ensure_ascii=False)
        print("✅ clasificacion_avanzada.json guardado")
        
        # 6. Guardar rutas de aprendizaje
        with open("data/processed/rutas_aprendizaje.json", "w", encoding="utf-8") as f:
            json.dump(scoring_result['rutas_aprendizaje'], f, indent=2, ensure_ascii=False)
        print("✅ rutas_aprendizaje.json guardado")
        
        # 7. Guardar recomendaciones personalizadas
        archivo_recomendaciones = f"data/processed/recomendaciones_{usuario_id}.json"
        with open(archivo_recomendaciones, "w", encoding="utf-8") as f:
            json.dump(recomendaciones, f, indent=2, ensure_ascii=False)
        print(f"✅ {archivo_recomendaciones} guardado")
        
        # 8. Guardar resumen ejecutivo
        resumen_ejecutivo = {
            "fecha_ejecucion": datetime.now().isoformat(),
            "usuario": usuario_id,
            "total_ofertas_analizadas": len(df_processed),
            "total_skills_identificadas": len(skills_count),
            "resumen_scoring": scoring_result['resumen'],
            "proxima_accion_recomendada": recomendaciones.get('proximo_paso', 'N/A'),
            "skills_criticas": recomendaciones.get('skills_criticas_para_aprender', [])
        }
        
        with open("data/processed/resumen_ejecutivo.json", "w", encoding="utf-8") as f:
            json.dump(resumen_ejecutivo, f, indent=2, ensure_ascii=False)
        print("✅ resumen_ejecutivo.json guardado")
        
    except Exception as e:
        print(f"❌ Error guardando resultados: {e}")
        return
    
    # PASO 9: MOSTRAR RESUMEN FINAL
    print("\n🎉 PIPELINE COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    
    print(f"📊 RESUMEN PARA {perfil_usuario.get('nombre', usuario_id)}:")
    print(f"   • 📈 Ofertas analizadas: {len(df_processed)}")
    print(f"   • 🎯 Skills identificadas: {len(skills_count)}")
    print(f"   • 💪 Skills que ya tienes: {scoring_result['resumen']['cobertura_actual']}")
    print(f"   • 📚 Skills para aprender: {scoring_result['resumen']['skills_para_aprender_urgente']}")
    print(f"   • 🚀 Próxima skill recomendada: {scoring_result['resumen']['proxima_skill_recomendada']}")
    print(f"   • 💡 Próximo paso: {recomendaciones.get('proximo_paso', 'N/A')}")
    
    if recomendaciones.get('skills_criticas_para_aprender'):
        print(f"\n🔴 SKILLS CRÍTICAS PARA APRENDER:")
        for i, skill in enumerate(recomendaciones['skills_criticas_para_aprender'][:3], 1):
            print(f"   {i}. {skill}")
    
    if scoring_result['rutas_aprendizaje']:
        print(f"\n🗺️  RUTAS DE APRENDIZAJE DISPONIBLES:")
        for ruta in scoring_result['rutas_aprendizaje'][:2]:
            print(f"   • {ruta['nombre']} ({ruta['timeline']})")
    
    print(f"\n💾 Resultados guardados en: data/processed/")
    print(f"📁 Archivos generados:")
    print(f"   - jobs_processed.csv (ofertas procesadas)")
    print(f"   - skills_count.csv (frecuencia skills)")
    print(f"   - scoring_skills.csv (scoring personalizado)")
    print(f"   - recomendaciones_{usuario_id}.json (recomendaciones)")
    print(f"   - rutas_aprendizaje.json (rutas de aprendizaje)")
    
    print(f"\n🎯 Próximos pasos:")
    print(f"   1. Revisar recomendaciones en data/processed/recomendaciones_{usuario_id}.json")
    print(f"   2. Ejecutar dashboard.py para visualización interactiva")
    print(f"   3. Actualizar tu perfil con nuevas skills adquiridas")

def ejecutar_modo_rapido():
    """
    Modo rápido para testing sin interacción de usuario
    """
    print("⚡ MODO RÁPIDO - EJECUCIÓN AUTOMÁTICA")
    
    try:
        # Extracción
        df_raw = extract_data()
        if df_raw.empty:
            print("❌ No hay datos para procesar")
            return
        
        # Transformación
        df_processed = transform_data(df_raw)
        
        # Análisis básico
        all_skills = []
        for _, row in df_processed.iterrows():
            all_skills.extend(row['skills_tecnicas'])
            all_skills.extend(row['skills_gestion'])
        
        skills_count = pd.Series(all_skills).value_counts().reset_index()
        skills_count.columns = ['skill', 'frecuencia']
        skills_count['porcentaje'] = (skills_count['frecuencia'] / len(df_processed) * 100).round(2)
        skills_count = skills_count.sort_values('frecuencia', ascending=False)
        
        # Guardar resultados básicos
        os.makedirs("data/processed", exist_ok=True)
        df_processed.to_csv("data/processed/jobs_processed.csv", index=False, encoding="utf-8-sig")
        skills_count.to_csv("data/processed/skills_count.csv", index=False, encoding="utf-8-sig")
        
        print(f"✅ Modo rápido completado:")
        print(f"   • {len(df_processed)} ofertas procesadas")
        print(f"   • {len(skills_count)} skills identificadas")
        print(f"   • Archivos guardados en data/processed/")
        
    except Exception as e:
        print(f"❌ Error en modo rápido: {e}")

if __name__ == "__main__":
    import sys
    
    # Verificar argumentos para modo rápido
    if len(sys.argv) > 1 and sys.argv[1] == "--rapido":
        ejecutar_modo_rapido()
    else:
        main()