# Documentación de la API

## 🔐 Autenticación

### Obtener Token de Acceso
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "tu_email@ejemplo.com",
  "password": "tu_password"
}