"""
Schema GraphQL extendido para reportes de veterinaria
"""
import strawberry
from typing import List, Optional
from datetime import datetime, date
from app.models.report_models import (
    ReporteFinanciero, ReporteClinico, ReporteOperacional,
    ReporteInventario, ReporteCompleto, FiltrosReporte,
    ConfiguracionReporte, TipoReporte, FormatoReporte,
    PeriodoReporte
)
from app.services.report_service import ReportService
from app.config.database import get_database


async def get_report_service():
    """Dependency para obtener el servicio de reportes"""
    async for db in get_database():
        yield ReportService(db)


@strawberry.type
class ReportQuery:
    """Consultas GraphQL para reportes"""
    
    @strawberry.field
    async def generar_reporte_financiero(
        self,
        fecha_inicio: date,
        fecha_fin: date,
        doctor_id: Optional[int] = None
    ) -> ReporteFinanciero:
        """Genera reporte financiero para el período especificado"""
        filtros = FiltrosReporte(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_reporte=TipoReporte.FINANCIERO,
            doctor_id=doctor_id
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_financiero(filtros)
    
    @strawberry.field
    async def generar_reporte_clinico(
        self,
        fecha_inicio: date,
        fecha_fin: date,
        doctor_id: Optional[int] = None,
        especie: Optional[str] = None
    ) -> ReporteClinico:
        """Genera reporte clínico para el período especificado"""
        filtros = FiltrosReporte(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_reporte=TipoReporte.CLINICO,
            doctor_id=doctor_id,
            especie=especie
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_clinico(filtros)
    
    @strawberry.field
    async def generar_reporte_operacional(
        self,
        fecha_inicio: date,
        fecha_fin: date
    ) -> ReporteOperacional:
        """Genera reporte operacional para el período especificado"""
        filtros = FiltrosReporte(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_reporte=TipoReporte.OPERACIONAL
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_operacional(filtros)
    
    @strawberry.field
    async def generar_reporte_inventario(
        self,
        fecha_inicio: date,
        fecha_fin: date
    ) -> ReporteInventario:
        """Genera reporte de inventario para el período especificado"""
        filtros = FiltrosReporte(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_reporte=TipoReporte.INVENTARIO
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_inventario(filtros)
    
    @strawberry.field
    async def generar_reporte_completo(
        self,
        fecha_inicio: date,
        fecha_fin: date,
        tipo_reporte: TipoReporte,
        incluir_graficos: bool = True,
        formato: FormatoReporte = FormatoReporte.PDF,
        doctor_id: Optional[int] = None,
        especie: Optional[str] = None
    ) -> ReporteCompleto:
        """Genera un reporte completo según los parámetros especificados"""
        
        filtros = FiltrosReporte(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_reporte=tipo_reporte,
            doctor_id=doctor_id,
            especie=especie,
            incluir_detalles=True
        )
        
        configuracion = ConfiguracionReporte(
            incluir_graficos=incluir_graficos,
            formato_exportacion=formato,
            incluir_comparaciones=True
        )
        
        async for report_service in get_report_service():
            return await report_service.generar_reporte_completo(filtros, configuracion)
    
    @strawberry.field
    async def obtener_tipos_reporte(self) -> List[str]:
        """Obtiene los tipos de reportes disponibles"""
        async for report_service in get_report_service():
            reportes = await report_service.obtener_reportes_disponibles()
            return [reporte["nombre"] for reporte in reportes]
    
    @strawberry.field
    async def reporte_comparativo_periodos(
        self,
        fecha_inicio_1: date,
        fecha_fin_1: date,
        fecha_inicio_2: date,
        fecha_fin_2: date,
        tipo_reporte: TipoReporte
    ) -> List[ReporteFinanciero]:
        """Genera reporte comparativo entre dos períodos"""
        
        # Período 1
        filtros_1 = FiltrosReporte(
            fecha_inicio=fecha_inicio_1,
            fecha_fin=fecha_fin_1,
            tipo_reporte=tipo_reporte
        )
        
        # Período 2
        filtros_2 = FiltrosReporte(
            fecha_inicio=fecha_inicio_2,
            fecha_fin=fecha_fin_2,
            tipo_reporte=tipo_reporte
        )
        
        async for report_service in get_report_service():
            if tipo_reporte == TipoReporte.FINANCIERO:
                reporte_1 = await report_service.generar_reporte_financiero(filtros_1)
                reporte_2 = await report_service.generar_reporte_financiero(filtros_2)
                return [reporte_1, reporte_2]
            
        return []
    
    @strawberry.field
    async def reportes_programados(self) -> List[str]:
        """Obtiene lista de reportes programados automáticamente"""
        # Implementar según necesidades de programación
        return [
            "Reporte Financiero Mensual",
            "Reporte de Vacunación Semanal",
            "Reporte Operacional Diario"
        ]


# Mutations para reportes (opcional)
@strawberry.type
class ReportMutation:
    """Mutations para operaciones de reportes"""
    
    @strawberry.field
    async def programar_reporte_automatico(
        self,
        tipo_reporte: TipoReporte,
        frecuencia: PeriodoReporte,
        email_destino: str,
        formato: FormatoReporte = FormatoReporte.PDF
    ) -> str:
        """Programa un reporte para generación automática"""
        
        # Implementar lógica de programación
        return f"Reporte {tipo_reporte.value} programado para envío {frecuencia.value} a {email_destino}"
    
    @strawberry.field
    async def cancelar_reporte_programado(
        self,
        id_programacion: str
    ) -> bool:
        """Cancela un reporte programado"""
        
        # Implementar lógica de cancelación
        return True
    
    @strawberry.field
    async def exportar_reporte(
        self,
        id_reporte: str,
        formato: FormatoReporte
    ) -> str:
        """Exporta un reporte existente en el formato especificado"""
        
        # Implementar lógica de exportación
        return f"Reporte exportado en formato {formato.value}"