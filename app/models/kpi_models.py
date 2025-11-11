"""
Modelos de KPIs usando Strawberry para GraphQL
"""
import strawberry
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


@strawberry.enum
class PeriodoKPI(Enum):
    """Períodos disponibles para los KPIs"""
    DIARIO = "diario"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    ANUAL = "anual"


@strawberry.enum
class EstadoCita(Enum):
    """Estados de las citas"""
    PENDIENTE = 1
    CONFIRMADA = 2
    COMPLETADA = 3
    CANCELADA = 4


@strawberry.type
class KPIBasico:
    """Tipo básico para KPIs simples"""
    valor: int
    porcentaje_cambio: Optional[float] = None
    fecha_calculo: datetime


@strawberry.type
class CitasPorMes:
    """KPI de citas agrupadas por mes"""
    mes: str
    anio: int
    total_citas: int
    citas_completadas: int
    citas_canceladas: int
    tasa_completitud: float


@strawberry.type
class MascotasPorEspecie:
    """KPI de mascotas agrupadas por especie"""
    especie: str
    total_mascotas: int
    porcentaje: float


@strawberry.type
class DoctorPerformance:
    """KPI de rendimiento por doctor"""
    doctor_id: int
    doctor_nombre: str
    total_citas: int
    citas_completadas: int
    tasa_completitud: float
    promedio_diagnosticos_por_cita: float


@strawberry.type
class VacunacionEstadisticas:
    """Estadísticas de vacunación"""
    total_vacunaciones: int
    vacunaciones_vencidas: int
    vacunaciones_proximas: int
    vacunas_mas_aplicadas: List[str]


@strawberry.type
class MascotasEstadisticas:
    """Estadísticas generales de mascotas"""
    total_mascotas: int
    nuevas_mascotas_mes: int
    distribucion_por_edad: List[str]
    mascotas_por_genero: List[str]


@strawberry.type
class IngresosEstimados:
    """KPI de ingresos estimados por período"""
    periodo: str
    total_citas: int
    ingreso_estimado: float
    crecimiento_porcentual: Optional[float] = None


@strawberry.type
class TendenciasMensuales:
    """Tendencias mensuales del negocio"""
    mes: str
    anio: int
    nuevos_clientes: int
    nuevas_mascotas: int
    total_citas: int
    citas_completadas: int
    vacunaciones: int


@strawberry.type
class AlertaVacunacion:
    """Alerta de vacunación próxima o vencida"""
    mascota_id: int
    mascota_nombre: str
    cliente_nombre: str
    cliente_telefono: str
    vacuna: str
    fecha_vencimiento: date
    dias_vencida: int
    urgencia: str


@strawberry.type
class DashboardResumen:
    """Resumen principal para el dashboard"""
    total_mascotas: int
    total_clientes: int
    total_doctores: int
    citas_hoy: int
    citas_semana: int
    vacunaciones_vencidas: int
    nuevos_clientes_mes: int
    tasa_ocupacion: float


@strawberry.type
class KPIDetallado:
    """KPI con más detalle y contexto"""
    nombre: str
    valor_actual: float
    valor_anterior: Optional[float] = None
    cambio_porcentual: Optional[float] = None
    tendencia: str  # "up", "down", "stable"
    unidad: str  # "cantidad", "porcentaje", "pesos", etc.
    descripcion: str
    fecha_actualizacion: datetime


@strawberry.type
class GraficoData:
    """Datos para gráficos en el dashboard"""
    etiqueta: str
    valor: float
    color: Optional[str] = None
    metadata: Optional[str] = None