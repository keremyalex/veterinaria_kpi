# 🚀 Inicio Rápido - Subgrafo KPI

## ⚡ **Problema Resuelto:**
- ✅ **Dependencias corregidas** en `requirements.txt`
- ✅ **Federation simplificada** (compatible con tu gateway)
- ✅ **Health check optimizado** sin curl
- ✅ **Puerto 9090** configurado

## ⚡ **Ejecutar en 3 Pasos:**

### 1️⃣ **Configurar BD:**
```bash
cd kpi-microservice
copy .env.example .env  # Windows
```

Editar `.env`:
```env
DATABASE_URL=postgresql://tu-user:tu-pass@tu-host:5432/veterinaria_db
POSTGRES_HOST=tu-host
POSTGRES_USER=tu-user  
POSTGRES_PASSWORD=tu-pass
POSTGRES_DB=veterinaria_db
```

### 2️⃣ **Ejecutar:**
```bash
docker-compose up --build
```

### 3️⃣ **Verificar:**
```bash
# Health check
curl http://localhost:9090/health

# Probar GraphQL
curl -X POST http://localhost:9090/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ health }"}'
```

## 🌐 **URLs del Subgrafo:**
- **GraphQL**: http://localhost:9090/graphql
- **Health**: http://localhost:9090/health
- **Docs**: http://localhost:9090/docs

## 🔗 **Configurar en Gateway:**
```javascript
// NestJS Gateway
{
  name: 'kpi-service',
  url: 'http://localhost:9090/graphql'
}
```

## 📊 **Consulta de Ejemplo:**
```graphql
query {
  dashboardResumen {
    totalMascotas
    totalClientes
    citasHoy
    vacunacionesVencidas
  }
}
```

¡Listo! Tu subgrafo KPI está ejecutándose en puerto 9090 🎉