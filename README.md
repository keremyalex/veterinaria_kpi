# Subgrafo de KPIs y Reportes para Sistema de Veterinaria

Subgrafo desarrollado en Python con FastAPI y GraphQL para proporcionar indicadores clave de rendimiento (KPIs) y sistema de reportes del sistema de veterinaria. Compatible con Apollo Federation.

## 🚀 Características

- **FastAPI**: Framework web moderno y de alto rendimiento
- **Strawberry GraphQL**: API GraphQL con soporte para Federation
- **Apollo Federation**: Compatible como subgrafo
- **PostgreSQL**: Conexión directa a la base de datos para consultas optimizadas
- **Docker**: Containerización completa con Docker Compose
- **KPIs en tiempo real**: Estadísticas actualizadas del negocio veterinario
- **Sistema de Reportes**: Generación de reportes financieros, clínicos y operacionales
- **Exportación múltiple**: PDF, Excel, CSV, JSON

## 📊 KPIs Disponibles

### Dashboard Principal
- Total de mascotas registradas
- Total de clientes activos
- Total de doctores
- Citas del día y de la semana
- Vacunaciones vencidas
- Tasa de ocupación

### Estadísticas Detalladas
- **Citas por mes**: Análisis mensual con tasas de completitud
- **Mascotas por especie**: Distribución porcentual
- **Performance de doctores**: Rendimiento individual por período
- **Estadísticas de vacunación**: Vencidas, próximas y más aplicadas
- **Alertas de vacunación**: Notificaciones por vencimientos

## � Reportes Disponibles

### Reporte Financiero
- Ingresos por servicio (consultas, vacunas, medicamentos, cirugías)
- Análisis de costos operativos
- Cálculo de ganancia neta y margen
- Comparación con períodos anteriores

### Reporte Clínico
- Total de consultas por período
- Distribución por tipo de servicio
- Diagnósticos más frecuentes
- Tratamientos aplicados
- Estadísticas de vacunación
- Tiempo promedio por consulta

### Reporte Operacional
- Ocupación de consultorios
- Utilización de equipos
- Tiempo de espera promedio
- Tasas de cancelación y reprogramación
- Eficiencia del personal

### Reporte de Inventario
- Medicamentos más utilizados
- Stock bajo y productos vencidos
- Rotación de inventario
- Análisis de costos y pérdidas

## �🛠️ Tecnologías

- **Python 3.11**
- **FastAPI 0.104+**
- **Strawberry GraphQL** con Federation
- **SQLAlchemy 2.0** (AsyncIO)
- **PostgreSQL** con AsyncPG
- **Pydantic 2.0** para validación
- **Docker & Docker Compose**
- **Apollo Federation** compatible
- **ReportLab** para PDFs
- **OpenPyXL** para Excel
- **Pandas** para análisis de datos
- **Matplotlib/Seaborn** para gráficos

## 📁 Estructura del Proyecto

```
veterinaria_kpi/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py      # Configuración de BD
│   │   └── settings.py      # Configuración general
│   ├── models/
│   │   ├── __init__.py
│   │   ├── kpi_models.py    # Modelos de KPIs
│   │   └── report_models.py # Modelos de Reportes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── kpi_service.py   # Lógica de KPIs
│   │   └── report_service.py# Lógica de Reportes
│   ├── graphql_schema/
│   │   ├── __init__.py
│   │   ├── schema.py        # Schema principal
│   │   └── report_schema.py # Schema de reportes
│   └── main.py              # Aplicación principal
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
│   │   ├── __init__.py
│   │   ├── database_models.py  # Modelos SQLAlchemy
│   │   └── kpi_models.py       # Tipos GraphQL
│   ├── services/
│   │   ├── __init__.py
│   │   └── kpi_service.py      # Lógica de negocio
│   ├── graphql_schema/
│   │   ├── __init__.py
│   │   └── schema.py           # Schema GraphQL
│   └── main.py                 # Aplicación principal
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init_db.py                 # Script de inicialización
├── .env.example
└── README.md
```

## 🚀 Instalación y Ejecución

### Prerequisitos
- Tu microservicio de base de datos PostgreSQL ejecutándose
- Docker (recomendado) o Python 3.11+

### Configuración de Conexión a BD Externa

```bash
# 1. Configurar variables de entorno
cp .env.example .env

# 2. Editar .env con los datos de tu BD existente
# DATABASE_URL=postgresql://user:pass@tu-host:5432/veterinaria_db
# POSTGRES_HOST=tu-host-o-ip
```

### Ejecución con Docker (Recomendado)

```bash
# Solo el servicio KPI (conecta a tu BD externa)
docker-compose up --build

# Ver logs
docker-compose logs -f kpi-service

# Detener
docker-compose down
```

### Ejecución Local (Solo si necesitas desarrollo sin Docker)

```bash
# Instalar Python 3.11+, luego:
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --host 0.0.0.0 --port 9090 --reload
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Base de datos
DATABASE_URL=postgresql://username:password@localhost:5432/veterinaria_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=veterinaria_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Servidor
HOST=0.0.0.0
PORT=8080
DEBUG=true

# GraphQL
ENABLE_INTROSPECTION=true
ENABLE_PLAYGROUND=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 🌐 API GraphQL (Subgrafo)

### Endpoints
- **GraphQL**: `http://localhost:9090/graphql`
- **SDL**: `http://localhost:9090/graphql/sdl` (para Federation)
- **Health Check**: `http://localhost:9090/health`

### Integración con Gateway

Este subgrafo debe ser registrado en tu Apollo Gateway existente:

```javascript
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'clinic-service', url: 'http://localhost:3001/graphql' },
      { name: 'kpi-service', url: 'http://localhost:9090/graphql' }
    ],
  }),
});
```

## 🔍 Ejemplos de Consultas GraphQL

### KPIs Básicos

```graphql
# Dashboard resumen
query Dashboard {
  dashboardResumen {
    totalMascotas
    totalClientes
    citasHoy
    ingresosMes
    crecimientoMensual
  }
}

# Citas por mes del año actual
query CitasMensuales {
  citasPorMes(anio: 2025) {
    mes
    anio
    totalCitas
    citasCompletadas
    tasaCompletitud
  }
}

# Performance de doctores
query PerformanceDoctores {
  doctorPerformance(mes: 11, anio: 2025) {
    doctorNombre
    totalCitas
    tasaCompletitud
    promedioDiagnosticosPorCita
  }
}
```

### Reportes Financieros

```graphql
# Reporte financiero mensual
query ReporteFinanciero {
  generarReporteFinanciero(
    fechaInicio: "2025-11-01"
    fechaFin: "2025-11-30"
  ) {
    periodo
    totalIngresos
    ingresosConsultas
    ingresosVacunas
    ingresosCirugia
    gananciaNeta
    margenGanancia
    comparacionPeriodoAnterior
  }
}
```

### Reportes Clínicos

```graphql
# Reporte clínico por doctor
query ReporteClinico {
  generarReporteClinico(
    fechaInicio: "2025-11-01"
    fechaFin: "2025-11-30"
    doctorId: 1
  ) {
    periodo
    totalConsultas
    consultasPorTipo
    diagnosticosFrecuentes
    vacunasAplicadas
    tiempoPromedioConsulta
    tasaSeguimiento
  }
}
```

### Reportes Operacionales

```graphql
# Análisis operacional
query ReporteOperacional {
  generarReporteOperacional(
    fechaInicio: "2025-11-01"
    fechaFin: "2025-11-30"
  ) {
    ocupacionConsultorios
    utilizacionEquipos
    tiempoEsperaPromedio
    cancelaciones
    tasaCancelacion
    eficienciaPersonal
  }
}
```

### Reportes Completos

```graphql
# Reporte completo con metadatos
query ReporteCompleto {
  generarReporteCompleto(
    fechaInicio: "2025-11-01"
    fechaFin: "2025-11-30"
    tipoReporte: FINANCIERO
    incluirGraficos: true
    formato: PDF
  ) {
    metadata {
      idReporte
      fechaGeneracion
      tiempoProcesamiento
      totalRegistros
    }
    resumen {
      puntosClave
      tendenciasPrincipales
      alertas
      recomendaciones
    }
    reporteFinanciero {
      totalIngresos
      gananciaNeta
      margenGanancia
    }
  }
}
```

### Comparación entre Períodos

```graphql
# Comparar dos trimestres
query ComparacionTrimestres {
  trimestre1: generarReporteFinanciero(
    fechaInicio: "2025-07-01"
    fechaFin: "2025-09-30"
  ) {
    totalIngresos
    gananciaNeta
  }
  
  trimestre2: generarReporteFinanciero(
    fechaInicio: "2025-10-01"
    fechaFin: "2025-12-31"
  ) {
    totalIngresos
    gananciaNeta
  }
}
```

## 🌐 API GraphQL (Subgrafo)

### Endpoints
- **GraphQL**: `http://localhost:9090/graphql`
- **SDL**: `http://localhost:9090/graphql/sdl` (para Federation)
- **Health Check**: `http://localhost:9090/health`

### Integración con Gateway

Este subgrafo debe ser registrado en tu Apollo Gateway existente:

```javascript
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'clinic-service', url: 'http://localhost:3001/graphql' },
      { name: 'kpi-service', url: 'http://localhost:9090/graphql' }
    ],
  }),
});
```

### Consultas desde Frontend (via Gateway)

```graphql
# Consulta unificada que combina datos operacionales y KPIs
query DashboardCompleto {
  # Datos del clinic-service
  doctores { id nombre apellido }
  
  # Datos del kpi-service  
  dashboardResumen {
    totalMascotas
    citasHoy
    ingresosMes
  }
  
  # Reportes combinados
  generarReporteFinanciero(
    fechaInicio: "2025-11-01"
    fechaFin: "2025-11-30"
  ) {
    totalIngresos
    margenGanancia
  }
}  
  dashboardResumen {
    totalMascotas
    citasHoy
    vacunacionesVencidas
  }
}
```

### Consultas Principales

```graphql
# Resumen del dashboard
query {
  dashboardResumen {
    totalMascotas
    totalClientes
    totalDoctores
    citasHoy
    citasSemana
    vacunacionesVencidas
    tasaOcupacion
  }
}

# Citas por mes
query {
  citasPorMes(año: 2024) {
    mes
    año
    totalCitas
    citasCompletadas
    tasaCompletitud
  }
}

# Performance de doctores
query {
  doctorPerformance(mes: 11, año: 2024) {
    doctorNombre
    totalCitas
    tasaCompletitud
    promedioDiagnosticosPorCita
  }
}

# Alertas de vacunación
query {
  alertasVacunacion(diasLimite: 30) {
    mascotaNombre
    clienteNombre
    clienteTelefono
    vacuna
    fechaVencimiento
    urgencia
  }
}
```

## 🏗️ Arquitectura

### Conexión Directa a Base de Datos

Este microservicio se conecta **directamente a PostgreSQL** en lugar de usar el gateway GraphQL principal por las siguientes razones:

1. **Optimización para Analytics**: Consultas complejas con agregaciones y JOINs
2. **Rendimiento**: Evita latencia adicional del gateway
3. **Especialización**: Queries específicas para reporting
4. **Independencia**: No depende del gateway para funcionar
5. **Escalabilidad**: Puede usar réplicas de solo lectura

### Integración con Frontend React

```javascript
// En tu componente React, consulta al gateway (no directamente al subgrafo)
import { useQuery } from '@apollo/client';

const DASHBOARD_QUERY = gql`
  query GetDashboard {
    # Datos combinados de múltiples subgrafos
    dashboardResumen {
      totalMascotas
      citasHoy
    }
    doctores {
      nombre
      apellido
    }
  }
`;

// Tu Apollo Client debe apuntar al gateway
const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql', // Gateway URL
  cache: new InMemoryCache()
});
```

## 📈 Vistas de Base de Datos Optimizadas

El script `init_db.py` crea vistas materializadas para optimizar las consultas:

- `vista_citas_mensuales`: Agregaciones mensuales de citas
- `vista_doctor_performance`: Métricas de rendimiento por doctor
- `vista_vacunaciones_proximas`: Alertas de vacunación

## 🔍 Monitoreo y Logs

```bash
# Ver logs del contenedor
docker-compose logs -f kpi-microservice

# Health check
curl http://localhost:8080/health
```

## 🚀 Deployment

### Producción con Docker

```bash
# Construir imagen para producción
docker build -t veterinaria/kpi-microservice:latest .

# Ejecutar en producción
docker run -d \
  --name kpi-service \
  -p 8080:8080 \
  --env-file .env.production \
  veterinaria/kpi-microservice:latest
```

### Variables de Producción

```env
DEBUG=false
ENABLE_INTROSPECTION=false
ENABLE_PLAYGROUND=false
ALLOWED_ORIGINS=https://tu-frontend.com
DATABASE_URL=postgresql://user:pass@prod-db:5432/veterinaria_db
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para reportar bugs o solicitar features, crear un issue en el repositorio.

---

**Desarrollado para el sistema de gestión veterinaria** 🐕🐱