# Consultas GraphQL del Subgrafo KPI

## 🚀 Configuración

Este subgrafo debe estar registrado en tu Apollo Gateway. Las consultas se realizan **a través del gateway**, no directamente al subgrafo.

- **Subgrafo KPI**: `http://localhost:8080/graphql`
- **Gateway**: `http://localhost:4000/graphql` (ejemplo)

## 📊 Consultas Principales (via Gateway)

### 1. Resumen del Dashboard

```graphql
query DashboardResumen {
  dashboardResumen {
    totalMascotas
    totalClientes
    totalDoctores
    citasHoy
    citasSemana
    vacunacionesVencidas
    nuevosClientesMes
    tasaOcupacion
  }
}
```

**Resultado esperado:**
```json
{
  "data": {
    "dashboardResumen": {
      "totalMascotas": 50,
      "totalClientes": 35,
      "totalDoctores": 3,
      "citasHoy": 5,
      "citasSemana": 23,
      "vacunacionesVencidas": 8,
      "nuevosClientesMes": 0,
      "tasaOcupacion": 31.25
    }
  }
}
```

### 2. Citas por Mes

```graphql
query CitasPorMes {
  citasPorMes(año: 2024) {
    mes
    año
    totalCitas
    citasCompletadas
    citasCanceladas
    tasaCompletitud
  }
}
```

### 3. Distribución de Mascotas por Especie

```graphql
query MascotasPorEspecie {
  mascotasPorEspecie {
    especie
    totalMascotas
    porcentaje
  }
}
```

### 4. Performance de Doctores

```graphql
query DoctorPerformance {
  doctorPerformance(mes: 11, año: 2024) {
    doctorId
    doctorNombre
    totalCitas
    citasCompletadas
    tasaCompletitud
    promedioDiagnosticosPorCita
  }
}
```

### 5. Estadísticas de Vacunación

```graphql
query VacunacionEstadisticas {
  vacunacionEstadisticas {
    totalVacunaciones
    vacunacionesVencidas
    vacunacionesProximas
    vacunasMasAplicadas
  }
}
```

### 6. Alertas de Vacunación

```graphql
query AlertasVacunacion {
  alertasVacunacion(diasLimite: 30) {
    mascotaId
    mascotaNombre
    clienteNombre
    clienteTelefono
    vacuna
    fechaVencimiento
    diasVencida
    urgencia
  }
}
```

### 7. Health Check

```graphql
query HealthCheck {
  health
}
```

## � Consultas Combinadas (Gateway + Multiple Subgrafos)

### Dashboard Completo con Datos Unificados
```graphql
query DashboardCompleto {
  # Datos del clinic-service (tu subgrafo existente)
  doctores {
    id
    nombre
    apellido
  }
  clientes {
    id
    nombre
  }
  
  # Datos del kpi-service (nuevo subgrafo)
  dashboardResumen {
    totalMascotas
    totalClientes
    citasHoy
    citasSemana
    vacunacionesVencidas
    tasaOcupacion
  }
  
  citasPorMes(año: 2024) {
    mes
    totalCitas
    tasaCompletitud
  }
  
  alertasVacunacion(diasLimite: 7) {
    mascotaNombre
    clienteNombre
    vacuna
    urgencia
  }
}
```

## 🧪 Consultas con Variables

### Citas por Período Específico
```graphql
query CitasPorPeriodo($año: Int, $mes: Int) {
  citasPorMes(año: $año) {
    mes
    año
    totalCitas
    citasCompletadas
    tasaCompletitud
  }
  
  doctorPerformance(mes: $mes, año: $año) {
    doctorNombre
    totalCitas
    tasaCompletitud
  }
}
```

**Variables:**
```json
{
  "año": 2024,
  "mes": 11
}
```

### Alertas por Urgencia
```graphql
query AlertasPorUrgencia($dias: Int) {
  alertasVacunacion(diasLimite: $dias) {
    mascotaNombre
    clienteNombre
    clienteTelefono
    vacuna
    fechaVencimiento
    urgencia
  }
}
```

**Variables:**
```json
{
  "dias": 15
}
```

## � Integración en Frontend

### Apollo Client Setup (apunta al Gateway)
```javascript
import { ApolloClient, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql', // Gateway URL, NO directamente al subgrafo
  cache: new InMemoryCache()
});
```

### Hook para Dashboard Unificado
```javascript
import { useQuery } from '@apollo/client';

const DASHBOARD_QUERY = gql`
  query DashboardCompleto {
    # Combina datos de clinic-service y kpi-service automáticamente
    doctores { nombre apellido }
    dashboardResumen { totalMascotas citasHoy }
    alertasVacunacion(diasLimite: 7) {
      mascotaNombre
      urgencia
    }
  }
`;

function Dashboard() {
  const { loading, error, data } = useQuery(DASHBOARD_QUERY);
  
  // El gateway combina automáticamente los datos de ambos subgrafos
  return (
    <div>
      <KPICards data={data.dashboardResumen} />
      <DoctorList doctors={data.doctores} />
      <AlertsList alerts={data.alertasVacunacion} />
    </div>
  );
}
```

## 🔧 Testing

### Probar el Subgrafo Directamente (solo para desarrollo)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ health }"}' \
  http://localhost:8080/graphql
```

### Probar via Gateway (producción)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ dashboardResumen { totalMascotas } }"}' \
  http://localhost:4000/graphql
```

## ⚙️ Configuración en Gateway

### NestJS Federation
```typescript
// app.module.ts
@Module({
  imports: [
    GraphQLGatewayModule.forRoot({
      gateway: {
        supergraphSdl: new IntrospectAndCompose({
          subgraphs: [
            { name: 'clinic-service', url: 'http://localhost:3001/graphql' },
            { name: 'kpi-service', url: 'http://localhost:8080/graphql' },
          ],
        }),
      },
    }),
  ],
})
export class AppModule {}
```

## 🚦 Códigos de Respuesta

- **200**: Consulta exitosa
- **400**: Error en la consulta GraphQL
- **500**: Error interno del servidor
- **503**: Base de datos no disponible

## 💡 Consejos de Optimización

1. **Usar fragmentos** para consultas repetitivas
2. **Polling** moderado para datos en tiempo real
3. **Cache** para datos que no cambian frecuentemente
4. **Paginación** para listas grandes (aunque no aplica mucho a KPIs)

```graphql
fragment ResumenBasico on DashboardResumen {
  totalMascotas
  totalClientes
  citasHoy
  tasaOcupacion
}

query {
  dashboardResumen {
    ...ResumenBasico
  }
}
```