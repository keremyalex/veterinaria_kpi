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
    total_citas: int = strawberry.field(name="totalCitas")
    citas_completadas: int = strawberry.field(name="citasCompletadas")
    citas_canceladas: int = strawberry.field(name="citasCanceladas")
    tasa_completitud: float = strawberry.field(name="tasaCompletitud")


@strawberry.type
class MascotasPorEspecie:
    """KPI de mascotas agrupadas por especie"""
    especie: str
    total_mascotas: int = strawberry.field(name="totalMascotas")
    porcentaje: float
    porcentaje: float


@strawberry.type
class DoctorPerformance:
    """KPI de rendimiento por doctor"""
    doctor_id: int = strawberry.field(name="doctorId")
    doctor_nombre: str = strawberry.field(name="doctorNombre")
    total_citas: int = strawberry.field(name="totalCitas")
    citas_completadas: int = strawberry.field(name="citasCompletadas")
    tasa_completitud: float = strawberry.field(name="tasaCompletitud")
    promedio_diagnosticos_por_cita: float = strawberry.field(name="promedioDiagnosticosPorCita")


@strawberry.type
class VacunacionEstadisticas:
    """Estadísticas de vacunación"""
    total_vacunaciones: int = strawberry.field(name="totalVacunaciones")
    vacunaciones_vencidas: int = strawberry.field(name="vacunacionesVencidas")
    vacunaciones_proximas: int = strawberry.field(name="vacunacionesProximas")
    vacunas_mas_aplicadas: List[str] = strawberry.field(name="vacunasMasAplicadas")


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
    mascota_id: int = strawberry.field(name="mascotaId")
    mascota_nombre: str = strawberry.field(name="mascotaNombre")
    cliente_nombre: str = strawberry.field(name="clienteNombre")
    tipo_vacuna: str = strawberry.field(name="tipoVacuna")
    fecha_ultima: Optional[str] = strawberry.field(name="fechaUltima", default=None)
    fecha_proxima: str = strawberry.field(name="fechaProxima")
    dias_vencimiento: int = strawberry.field(name="diasVencimiento")
    prioridad: str


@strawberry.type
class DashboardResumen:
    """Resumen principal para el dashboard"""
    total_mascotas: int = strawberry.field(name="totalMascotas")
    total_clientes: int = strawberry.field(name="totalClientes") 
    total_citas: int = strawberry.field(name="totalCitas")
    citas_hoy: int = strawberry.field(name="citasHoy")
    ingresos_mes: float = strawberry.field(name="ingresosMes")
    crecimiento_mensual: Optional[float] = strawberry.field(name="crecimientoMensual", default=None)


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