# Configuración para Base de Datos Externa

## 🗄️ **Conexión a tu BD Existente**

Este subgrafo KPI se conecta **directamente a tu base de datos PostgreSQL existente** donde ya tienes los datos de la clínica.

### ⚙️ **Configuración Requerida**

#### 1. **Archivo .env:**
```env
# Datos de tu base de datos existente
DATABASE_URL=postgresql://tu-usuario:tu-password@tu-host:5432/veterinaria_db
POSTGRES_HOST=tu-host-o-ip          # IP del servidor BD o nombre del contenedor
POSTGRES_PORT=5432                  # Puerto de tu PostgreSQL
POSTGRES_USER=tu-usuario            # Usuario de tu BD
POSTGRES_PASSWORD=tu-password       # Contraseña de tu BD
POSTGRES_DB=veterinaria_db          # Nombre de tu base de datos

# Configuración del subgrafo KPI
PORT=8080
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000

# Federation
GATEWAY_URL=http://localhost:4000/graphql
```

#### 2. **Ejemplos según tu setup:**

**Si tu BD está en Docker:**
```env
POSTGRES_HOST=nombre-contenedor-bd
# o
POSTGRES_HOST=172.17.0.1  # IP de Docker host
```

**Si tu BD está en localhost:**
```env
POSTGRES_HOST=host.docker.internal  # Desde container a localhost
# o
POSTGRES_HOST=localhost              # Si ejecutas sin Docker
```

**Si tu BD está en servidor remoto:**
```env
POSTGRES_HOST=192.168.1.100         # IP del servidor
```

### 🚀 **Ejecución según tu Arquitectura**

#### **Opción A: Todo en Docker**
```bash
# Si tu BD también está en Docker
docker-compose -f docker-compose.dev.yml up --build
```

#### **Opción B: BD externa, KPI en Docker**
```bash
# Configurar .env con host de tu BD
docker-compose up --build
```

#### **Opción C: Todo local**
```bash
# Si ejecutas todo en local
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 🔧 **Script init_db.py**

Este script **NO crea tablas** (porque ya existen), solo crea:
- ✅ **Vistas optimizadas** para KPIs
- ✅ **Índices** para consultas rápidas  
- ✅ **Funciones agregadas** para reportes

**Es seguro ejecutarlo** en tu BD existente.

### 🌐 **Integración con tu Gateway**

Una vez ejecutándose:

```javascript
// En tu gateway NestJS
const subgraphs = [
  {
    name: 'clinic-service',
    url: 'http://localhost:3001/graphql'  // Tu servicio actual
  },
  {
    name: 'kpi-service', 
    url: 'http://localhost:9090/graphql'  // Nuevo subgrafo KPI
  }
];
```

### 🔍 **Verificación**

```bash
# 1. Verificar que el servicio está corriendo
curl http://localhost:9090/health

# 2. Probar una consulta KPI
curl -X POST http://localhost:9090/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ dashboardResumen { totalMascotas } }"}'

# 3. Verificar SDL para Federation
curl http://localhost:9090/graphql/sdl
```

### ⚠️ **Consideraciones Importantes**

1. **Permisos de BD**: El usuario debe tener permisos de SELECT en todas las tablas
2. **Firewall**: Asegurar que el puerto de PostgreSQL esté accesible
3. **Red Docker**: Si ambos están en Docker, deben estar en la misma red
4. **Conexiones**: PostgreSQL debe permitir conexiones desde la IP del container

### 🔒 **Seguridad**

- ✅ Solo acceso de **LECTURA** a la base de datos
- ✅ **No modifica** datos existentes
- ✅ **Aislado** del microservicio principal
- ✅ Usa usuario con **permisos limitados**