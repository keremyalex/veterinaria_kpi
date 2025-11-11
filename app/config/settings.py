from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings
    """
    # Base de datos
    database_url: str = "postgresql://username:password@localhost:5432/veterinaria_db"
    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_db: str = "veterinaria_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # Servidor
    host: str = "0.0.0.0"
    port: int = 9090
    debug: bool = True
    
    # GraphQL
    enable_introspection: bool = True
    enable_playground: bool = True
    
    # CORS
    allowed_origins: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:4000"  # Gateway
    ]
    
    @field_validator('allowed_origins')
    @classmethod
    def parse_cors_origins(cls, v):
        """Convierte la cadena de orígenes separada por comas en una lista"""
        if isinstance(v, str):
            # Si viene como string desde .env, la separamos por comas
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # API
    api_title: str = "Veterinaria KPI Subgraph"
    api_description: str = "Subgrafo de KPIs para Apollo Federation - Sistema de Veterinaria"
    api_version: str = "1.0.0"
    
    # Federation
    federation_version: str = "2.0"
    subgraph_name: str = "kpi-service"
    gateway_url: str = "http://localhost:4000/graphql"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignora variables de entorno extra no definidas

    def get_database_url(self) -> str:
        """Construye la URL de la base de datos"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# Instancia global de configuración
settings = Settings()