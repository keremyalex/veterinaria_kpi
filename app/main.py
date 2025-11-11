"""
Aplicación principal del microservicio de KPIs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.config.database import test_connection, close_database
from app.graphql_schema.schema import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    # Startup
    print("🚀 Iniciando microservicio de KPIs...")
    
    # Probar conexión a la base de datos
    db_connected = await test_connection()
    if not db_connected:
        print("❌ No se pudo conectar a la base de datos")
        # En producción, podrías querer fallar aquí
    
    print("✅ Microservicio de KPIs iniciado correctamente")
    yield
    
    # Shutdown
    print("🔒 Cerrando microservicio de KPIs...")
    await close_database()
    print("✅ Microservicio cerrado correctamente")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Router GraphQL
graphql_router = GraphQLRouter(
    schema,
    graphiql=settings.enable_playground,
)

# Incluir router GraphQL
app.include_router(graphql_router, prefix="/graphql")


@app.get("/")
async def root():
    """Endpoint raíz del subgrafo KPI"""
    return {
        "service": "Veterinaria KPI Subgraph",
        "version": settings.api_version,
        "subgraph": settings.subgraph_name,
        "federation_version": settings.federation_version,
        "graphql_endpoint": "/graphql",
        "sdl_endpoint": "/graphql/sdl",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check del microservicio"""
    try:
        db_status = await test_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "timestamp": "2024-11-11T00:00:00Z",
            "version": settings.api_version
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": "2024-11-11T00:00:00Z",
            "version": settings.api_version
        }