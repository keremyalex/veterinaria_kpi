"""
Schema GraphQL para KPIs de veterinaria - Compatible con Apollo Federation
Incluye funcionalidades de KPIs y Reportes
"""
import strawberry
from typing import List, Optional
from datetime import datetime, date
from app.models.kpi_models import (
    CitasPorMes, MascotasPorEspecie, DoctorPerformance,
    VacunacionEstadisticas, DashboardResumen, AlertaVacunacion
)
from app.models.report_models import (
    ReporteFinanciero, ReporteClinico, ReporteOperacional,
    ReporteInventario, ReporteCompleto, TipoReporte, FormatoReporte
)
from app.services.kpi_service_real import KPIServiceReal
from app.services.report_service import ReportService
from app.config.database import get_database


async def get_kpi_service():
    """Dependency para obtener el servicio de KPIs REAL"""
    async for db in get_database():
        yield KPIServiceReal(db)


async def get_report_service():
    """Dependency para obtener el servicio de reportes"""
    async for db in get_database():
        yield ReportService(db)


# Tipo _Service requerido por Apollo Federation
@strawberry.type
class _Service:
    sdl: str


@strawberry.type
class Query:
    """
    Consultas GraphQL para KPIs y Reportes de la veterinaria
    Compatible con Apollo Federation
    """

    # Campo _service requerido por Apollo Federation
    @strawberry.field(name="_service")
    def service_field(self) -> _Service:
        """Campo _service requerido por Apollo Federation para composición del schema"""
        sdl = '''
            type Query {
                # KPIs
                dashboardResumen: DashboardResumen!
                citasPorMes(anio: Int): [CitasPorMes!]!
                estadisticasMascotasPorEspecie: [MascotasPorEspecie!]!
                doctorPerformance(mes: Int, anio: Int): [DoctorPerformance!]!
                vacunacionEstadisticas: VacunacionEstadisticas!
                alertasVacunacion(diasLimite: Int = 30): [AlertaVacunacion!]!
                health: String!
                
                # Reportes
                generarReporteFinanciero(fechaInicio: Date!, fechaFin: Date!, doctorId: Int): ReporteFinanciero!
                generarReporteClinico(fechaInicio: Date!, fechaFin: Date!, doctorId: Int, especie: String): ReporteClinico!
                generarReporteOperacional(fechaInicio: Date!, fechaFin: Date!): ReporteOperacional!
                generarReporteInventario(fechaInicio: Date!, fechaFin: Date!): ReporteInventario!
                generarReporteCompleto(fechaInicio: Date!, fechaFin: Date!, tipoReporte: TipoReporte!, incluirGraficos: Boolean = true, formato: FormatoReporte = PDF, doctorId: Int, especie: String): ReporteCompleto!
                obtenerTiposReporte: [String!]!
            }

            # Tipos KPI
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

            # Tipos Reportes
            type ReporteFinanciero {
                periodo: String!
                fechaInicio: Date!
                fechaFin: Date!
                ingresosConsultas: Float!
                ingresosVacunas: Float!
                ingresosMedicamentos: Float!
                ingresosCirugia: Float!
                totalIngresos: Float!
                costosOperativos: Float!
                gananciaNeta: Float!
                margenGanancia: Float!
                comparacionPeriodoAnterior: Float!
            }

            type ReporteClinico {
                periodo: String!
                fechaInicio: Date!
                fechaFin: Date!
                totalConsultas: Int!
                consultasPorTipo: [String!]!
                diagnosticosFrecuentes: [String!]!
                tratamientosAplicados: [String!]!
                cirugiasRealizadas: Int!
                vacunasAplicadas: Int!
                tiempoPromedioConsulta: Float!
                tasaSeguimiento: Float!
            }

            type ReporteOperacional {
                periodo: String!
                fechaInicio: Date!
                fechaFin: Date!
                ocupacionConsultorios: Float!
                utilizacionEquipos: Float!
                tiempoEsperaPromedio: Float!
                cancelaciones: Int!
                tasaCancelacion: Float!
                reprogramaciones: Int!
                satisfaccionCliente: Float
                eficienciaPersonal: Float!
            }

            type ReporteInventario {
                periodo: String!
                fechaInicio: Date!
                fechaFin: Date!
                medicamentosUtilizados: [String!]!
                stockBajo: [String!]!
                productosVencidos: [String!]!
                rotacionInventario: Float!
                costoInventario: Float!
                perdidasVencimiento: Float!
            }

            type ReporteCompleto {
                metadata: MetadataReporte!
                resumen: ResumenReporte!
                reporteFinanciero: ReporteFinanciero
                reporteClinico: ReporteClinico
                reporteOperacional: ReporteOperacional
                reporteInventario: ReporteInventario
            }

            type MetadataReporte {
                idReporte: String!
                fechaGeneracion: String!
                usuarioSolicitante: String!
                tiempoProcesamiento: Float!
                totalRegistros: Int!
                filtrosAplicados: String!
            }

            type ResumenReporte {
                puntosClave: [String!]!
                tendenciasPrincipales: [String!]!
                alertas: [String!]!
                recomendaciones: [String!]!
                metricasDestacadas: [String!]!
            }

            enum TipoReporte {
                FINANCIERO
                CLINICO
                OPERACIONAL
                MARKETING
                INVENTARIO
            }

            enum FormatoReporte {
                PDF
                EXCEL
                CSV
                JSON
            }

            scalar Date
        '''
        return _Service(sdl=sdl.strip())

    # === KPI QUERIES ===
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
    async def estadisticasMascotasPorEspecie(self) -> List[MascotasPorEspecie]:
        """Obtiene estadísticas de mascotas agrupadas por especie"""
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
        return "KPI & Reports Subgraph is running! 🚀📊"

    # === REPORT QUERIES ===
    @strawberry.field
    async def generarReporteFinanciero(
        self,
        fechaInicio: date,
        fechaFin: date,
        doctorId: Optional[int] = None
    ) -> ReporteFinanciero:
        """Genera reporte financiero para el período especificado"""
        from app.models.report_models import FiltrosReporte
        
        filtros = FiltrosReporte(
            fecha_inicio=fechaInicio,
            fecha_fin=fechaFin,
            tipo_reporte=TipoReporte.FINANCIERO,
            doctor_id=doctorId
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_financiero(filtros)

    @strawberry.field
    async def generarReporteClinico(
        self,
        fechaInicio: date,
        fechaFin: date,
        doctorId: Optional[int] = None,
        especie: Optional[str] = None
    ) -> ReporteClinico:
        """Genera reporte clínico para el período especificado"""
        from app.models.report_models import FiltrosReporte
        
        filtros = FiltrosReporte(
            fecha_inicio=fechaInicio,
            fecha_fin=fechaFin,
            tipo_reporte=TipoReporte.CLINICO,
            doctor_id=doctorId,
            especie=especie
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_clinico(filtros)

    @strawberry.field
    async def generarReporteOperacional(
        self,
        fechaInicio: date,
        fechaFin: date
    ) -> ReporteOperacional:
        """Genera reporte operacional para el período especificado"""
        from app.models.report_models import FiltrosReporte
        
        filtros = FiltrosReporte(
            fecha_inicio=fechaInicio,
            fecha_fin=fechaFin,
            tipo_reporte=TipoReporte.OPERACIONAL
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_operacional(filtros)

    @strawberry.field
    async def generarReporteInventario(
        self,
        fechaInicio: date,
        fechaFin: date
    ) -> ReporteInventario:
        """Genera reporte de inventario para el período especificado"""
        from app.models.report_models import FiltrosReporte
        
        filtros = FiltrosReporte(
            fecha_inicio=fechaInicio,
            fecha_fin=fechaFin,
            tipo_reporte=TipoReporte.INVENTARIO
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_inventario(filtros)

    @strawberry.field
    async def generarReporteCompleto(
        self,
        fechaInicio: date,
        fechaFin: date,
        tipoReporte: TipoReporte,
        incluirGraficos: bool = True,
        formato: FormatoReporte = FormatoReporte.PDF,
        doctorId: Optional[int] = None,
        especie: Optional[str] = None
    ) -> ReporteCompleto:
        """Genera un reporte completo según los parámetros especificados"""
        from app.models.report_models import FiltrosReporte, ConfiguracionReporte
        
        filtros = FiltrosReporte(
            fecha_inicio=fechaInicio,
            fecha_fin=fechaFin,
            tipo_reporte=tipoReporte,
            doctor_id=doctorId,
            especie=especie,
            incluir_detalles=True
        )
        
        configuracion = ConfiguracionReporte(
            incluir_graficos=incluirGraficos,
            formato_exportacion=formato,
            incluir_comparaciones=True
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_completo(filtros, configuracion)

    @strawberry.field
    async def obtenerTiposReporte(self) -> List[str]:
        """Obtiene los tipos de reportes disponibles"""
        async for report_service in get_report_service():
            reportes = await report_service.obtener_reportes_disponibles()
            return [reporte["nombre"] for reporte in reportes]


# Schema principal - Compatible con Apollo Federation
schema = strawberry.Schema(query=Query)