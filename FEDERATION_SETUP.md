# Configuración del Subgrafo KPI para Apollo Federation

## 🌐 **Arquitectura como Subgrafo**

Tu microservicio de KPIs ahora funciona como un **subgrafo** en Apollo Federation:

```
┌─────────────────┐    ┌──────────────────┐    
│   React App     │────│  Apollo Gateway  │    
│   (Frontend)    │    │  (Federation)    │    
└─────────────────┘    └─────────┬────────┘    
                                 │             
                    ┌────────────┼────────────┐
                    │            │            │
               ┌────▼────┐  ┌────▼────┐  ┌───▼────┐
               │ Clinic  │  │   KPI   │  │ Other  │
               │Subgraph │  │Subgraph │  │Subgraph│
               │(Nest.js)│  │(Python) │  │        │
               └─────────┘  └─────────┘  └────────┘
                     │            │            │
                     └────────────┼────────────┘
                                  │
                        ┌─────────▼─────────┐
                        │   PostgreSQL      │
                        │   Database        │
                        └───────────────────┘
```

## 🔧 **Configuración en tu Gateway**

### 1. **Agregar el subgrafo KPI a tu gateway:**

Si usas Apollo Gateway (Node.js), agrega esto a tu configuración:

\`\`\`javascript
// gateway.js
const { ApolloGateway } = require('@apollo/gateway');
const { ApolloServer } = require('apollo-server-express');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      {
        name: 'clinic-service',
        url: 'http://localhost:3001/graphql', // Tu servicio existente
      },
      {
        name: 'kpi-service',
        url: 'http://localhost:8080/graphql', // Nuevo subgrafo KPI
      }
    ],
  }),
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
});
\`\`\`

### 2. **Si usas NestJS con Federation:**

\`\`\`typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { GraphQLGatewayModule } from '@nestjs/graphql';
import { IntrospectAndCompose } from '@apollo/gateway';

@Module({
  imports: [
    GraphQLGatewayModule.forRoot({
      gateway: {
        supergraphSdl: new IntrospectAndCompose({
          subgraphs: [
            {
              name: 'clinic-service',
              url: 'http://localhost:3001/graphql',
            },
            {
              name: 'kpi-service', 
              url: 'http://localhost:8080/graphql',
            },
          ],
        }),
      },
    }),
  ],
})
export class AppModule {}
\`\`\`

## 📊 **Consultas desde tu Frontend**

Ahora desde tu React puedes hacer consultas unificadas:

\`\`\`graphql
# Consulta que combina datos del clinic-service y kpi-service
query DashboardCompleto {
  # Datos del clinic-service (existente)
  doctores {
    id
    nombre
    apellido
  }
  
  # Datos del kpi-service (nuevo)
  dashboardResumen {
    totalMascotas
    totalClientes
    citasHoy
    vacunacionesVencidas
  }
  
  citasPorMes(año: 2024) {
    mes
    totalCitas
    tasaCompletitud
  }
}
\`\`\`

## 🚀 **Para Ejecutar el Subgrafo KPI:**

\`\`\`bash
cd kpi-microservice

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus datos de BD

# Opción 1: Python local
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8080

# Opción 2: Docker
docker-compose up --build
\`\`\`

## 🔗 **Endpoints del Subgrafo:**

- **GraphQL**: \`http://localhost:8080/graphql\`
- **SDL**: \`http://localhost:8080/graphql/sdl\` (para Federation)
- **Health**: \`http://localhost:8080/health\`

## ✅ **Ventajas de esta Arquitectura:**

1. **Frontend unificado**: Una sola consulta GraphQL
2. **Separación de responsabilidades**: KPIs en Python, lógica de negocio en NestJS
3. **Escalabilidad independiente**: Cada subgrafo puede escalar por separado
4. **Tecnologías especializadas**: Python para analytics, NestJS para CRUD
5. **Conexión directa**: KPIs van directo a BD para mejor performance

## 🧪 **Probar la Integración:**

1. **Ejecuta tu gateway** existente
2. **Ejecuta el subgrafo KPI** en puerto 8080
3. **Consulta desde tu React** al gateway (puerto 4000 o el que uses)

El gateway automáticamente combinará los esquemas y podrás hacer consultas que incluyan tanto datos operacionales como KPIs.

## 📝 **Próximos Pasos:**

1. Configurar el subgrafo KPI en tu gateway
2. Actualizar tu frontend para incluir las nuevas queries de KPIs  
3. Agregar componentes de dashboard con los datos obtenidos

¿Necesitas ayuda configurando esto en tu gateway existente?