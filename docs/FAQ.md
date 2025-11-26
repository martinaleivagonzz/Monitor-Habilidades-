
```markdown
# ❓ Preguntas Frecuentes

## **Generales**

### ¿Qué datos utiliza SkillMonitor?
Analizamos ofertas laborales de portales chilenos como Indeed, Computrabajo y LinkedIn, procesando habilidades técnicas requeridas y tendencias de contratación.

### ¿Es gratuito?
Sí, la versión actual es completamente gratuita para estudiantes y profesionales.

### ¿Con qué frecuencia se actualizan los datos?
El sistema actualiza la base de datos cada 24 horas automáticamente.

## 🔧 Técnicas

### ¿Qué versión de Python necesito?
Python 3.8 o superior. Recomendamos Python 3.10 para mejor rendimiento.

### ¿Puedo usar otra base de datos?
Actualmente solo soportamos MongoDB como base principal, pero estamos trabajando en soporte para PostgreSQL.

### ¿Cómo manejan la escalabilidad?
Usamos Redis para cache y session storage, y nuestra arquitectura permite escalamiento horizontal.

## **Datos y Privacidad**

### ¿Qué hacen con mis datos de perfil?
Tus datos son completamente privados. Solo los usamos para generar tus recomendaciones personales y no los compartimos con terceros.

### ¿Los datos del mercado son en tiempo real?
Sí, procesamos ofertas laborales en tiempo real con un desfase máximo de 24 horas.

### ¿Cubren todo Chile?
Actualmente nos enfocamos en las principales regiones metropolitanas, pero estamos expandiendo cobertura.