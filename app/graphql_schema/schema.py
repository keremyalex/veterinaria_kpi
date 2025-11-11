"""
Schema GraphQL para KPIs de veterinaria - Compatible con Apollo Federation
"""
import strawberry
from typing import List, Optional
from datetime import datetime
from app.models.kpi_models import (
    CitasPorMes, MascotasPorEspecie, DoctorPerformance,
    VacunacionEstadisticas, DashboardResumen, AlertaVacunacion
)
from app.services.kpi_service import KPIService
from app.config.database import get_database


async def get_kpi_service():
    """Dependency para obtener el servicio de KPIs"""
    async for db in get_database():
        yield KPIService(db)


# Tipo _Service requerido por Apollo Federation
@strawberry.type
class _Service:
    sdl: str


@strawberry.type
class Query:
    """
    Consultas GraphQL para KPIs de la veterinaria
    Compatible con Apollo Federation
    """

    # Campo _service requerido por Apollo Federation
    @strawberry.field(name="_service")
    def service_field(self) -> _Service:
        """Campo _service requerido por Apollo Federation para composición del schema"""
        sdl = '''
            type Query {
                dashboardResumen: DashboardResumen!
                citasPorMes(anio: Int): [CitasPorMes!]!
                mascotasPorEspecie: [MascotasPorEspecie!]!
                doctorPerformance(mes: Int, anio: Int): [DoctorPerformance!]!
                vacunacionEstadisticas: VacunacionEstadisticas!
                alertasVacunacion(diasLimite: Int = 30): [AlertaVacunacion!]!
                health: String!
            }

            type DashboardResumen {
                totalMascotas: Int!
                totalCitas: Int!
                totalClientes: Int!
                citasHoy: Int!
                ingresosMes: Float!
                crecimientoMensual: Float
            }

            type CitasPorMes {
                mes: String!
                anio: Int!
                totalCitas: Int!
                citasCompletadas: Int!
                citasCanceladas: Int!
                tasaCompletitud: Float!
            }

            type MascotasPorEspecie {
                especie: String!
                totalMascotas: Int!
                porcentaje: Float!
            }

            type DoctorPerformance {
                doctorId: Int!
                doctorNombre: String!
                totalCitas: Int!
                citasCompletadas: Int!
                tasaCompletitud: Float!
                promedioDiagnosticosPorCita: Float!
            }

            type VacunacionEstadisticas {
                totalVacunaciones: Int!
                vacunacionesVencidas: Int!
                vacunacionesProximas: Int!
                vacunasMasAplicadas: [String!]!
            }

            type AlertaVacunacion {
                mascotaId: Int!
                mascotaNombre: String!
                clienteNombre: String!
                tipoVacuna: String!
                fechaUltima: String
                fechaProxima: String!
                diasVencimiento: Int!
                prioridad: String!
            }
        '''
        return _Service(sdl=sdl.strip())

    @strawberry.field
    async def dashboardResumen(self) -> DashboardResumen:
        """Obtiene el resumen principal del dashboard"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_dashboard_resumen()

    @strawberry.field
    async def citasPorMes(self, anio: Optional[int] = None) -> List[CitasPorMes]:
        """Obtiene estadísticas de citas agrupadas por mes"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_citas_por_mes(anio)

    @strawberry.field
    async def mascotasPorEspecie(self) -> List[MascotasPorEspecie]:
        """Obtiene distribución de mascotas por especie"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_mascotas_por_especie()

    @strawberry.field
    async def doctorPerformance(
        self, 
        mes: Optional[int] = None, 
        anio: Optional[int] = None
    ) -> List[DoctorPerformance]:
        """Obtiene estadísticas de rendimiento por doctor"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_doctor_performance(mes, anio)

    @strawberry.field
    async def vacunacionEstadisticas(self) -> VacunacionEstadisticas:
        """Obtiene estadísticas de vacunación"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_vacunacion_estadisticas()

    @strawberry.field
    async def alertasVacunacion(self, diasLimite: int = 30) -> List[AlertaVacunacion]:
        """Obtiene alertas de vacunaciones próximas o vencidas"""
        async for kpi_service in get_kpi_service():
            return await kpi_service.get_alertas_vacunacion(diasLimite)

    @strawberry.field
    async def health(self) -> str:
        """Health check del servicio KPI"""
        return "KPI Subgraph is running! 🚀"


# Schema principal - Compatible con Apollo Federation
schema = strawberry.Schema(query=Query)