"""
Modelos específicos para reportes de veterinaria
"""
import strawberry
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
from decimal import Decimal


@strawberry.enum
class TipoReporte(Enum):
    """Tipos de reportes disponibles"""
    FINANCIERO = "financiero"
    CLINICO = "clinico"
    OPERACIONAL = "operacional"
    MARKETING = "marketing"
    INVENTARIO = "inventario"


@strawberry.enum
class FormatoReporte(Enum):
    """Formatos de exportación"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"


@strawberry.enum
class PeriodoReporte(Enum):
    """Períodos para reportes"""
    DIARIO = "diario"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"
    PERSONALIZADO = "personalizado"


@strawberry.type
class ReporteFinanciero:
    """Reporte financiero detallado"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    ingresos_consultas: float
    ingresos_vacunas: float
    ingresos_medicamentos: float
    ingresos_cirugia: float
    total_ingresos: float
    costos_operativos: float
    ganancia_neta: float
    margen_ganancia: float
    comparacion_periodo_anterior: float


@strawberry.type
class ReporteClinico:
    """Reporte clínico y médico"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    total_consultas: int
    consultas_por_tipo: List[str]  # JSON con tipos y cantidades
    diagnosticos_frecuentes: List[str]
    tratamientos_aplicados: List[str]
    cirugias_realizadas: int
    vacunas_aplicadas: int
    tiempo_promedio_consulta: float
    tasa_seguimiento: float


@strawberry.type
class ReporteOperacional:
    """Reporte operacional del centro veterinario"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    ocupacion_consultorios: float
    utilizacion_equipos: float
    tiempo_espera_promedio: float
    cancelaciones: int
    tasa_cancelacion: float
    reprogramaciones: int
    satisfaccion_cliente: Optional[float]
    eficiencia_personal: float


@strawberry.type
class ReporteInventario:
    """Reporte de inventario y medicamentos"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    medicamentos_utilizados: List[str]  # JSON con medicamentos y cantidades
    stock_bajo: List[str]
    productos_vencidos: List[str]
    rotacion_inventario: float
    costo_inventario: float
    perdidas_vencimiento: float


@strawberry.type
class ReporteCliente:
    """Reporte de análisis de clientes"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    clientes_nuevos: int
    clientes_recurrentes: int
    clientes_inactivos: int
    valor_promedio_cliente: float
    frecuencia_visitas: float
    retencion_clientes: float
    satisfaccion_promedio: Optional[float]


@strawberry.type
class ReporteMascota:
    """Reporte de análisis de mascotas"""
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    mascotas_nuevas: int
    mascotas_por_especie: List[str]  # JSON
    mascotas_por_raza: List[str]  # JSON
    mascotas_por_edad: List[str]  # JSON
    vacunacion_al_dia: int
    mascotas_enfermas_cronicas: int
    tratamientos_en_curso: int


@strawberry.type
class ReporteComparativo:
    """Reporte comparativo entre períodos"""
    periodo_actual: str
    periodo_anterior: str
    metricas_comparadas: List[str]  # JSON con métricas y cambios
    crecimiento_ingresos: float
    crecimiento_clientes: float
    crecimiento_mascotas: float
    cambio_eficiencia: float
    tendencias: List[str]


@strawberry.type
class ReportePredictivo:
    """Reporte con análisis predictivo"""
    periodo_proyeccion: str
    ingresos_proyectados: float
    clientes_proyectados: int
    demanda_servicios: List[str]  # JSON con servicios y demanda proyectada
    necesidades_personal: str
    recomendaciones: List[str]
    confianza_prediccion: float


@strawberry.type
class ReportePersonalizado:
    """Reporte personalizado por usuario"""
    nombre_reporte: str
    usuario_creador: str
    filtros_aplicados: List[str]
    metricas_seleccionadas: List[str]
    datos: List[str]  # JSON con los datos del reporte
    fecha_generacion: datetime
    parametros: Optional[str]  # JSON con parámetros del reporte


@strawberry.input
class FiltrosReporte:
    """Filtros para generar reportes"""
    fecha_inicio: date
    fecha_fin: date
    tipo_reporte: TipoReporte
    doctor_id: Optional[int] = None
    cliente_id: Optional[int] = None
    especie: Optional[str] = None
    servicio: Optional[str] = None
    estado_cita: Optional[int] = None
    incluir_canceladas: bool = False
    incluir_detalles: bool = True


@strawberry.input
class ConfiguracionReporte:
    """Configuración para generar reportes"""
    titulo_personalizado: Optional[str] = None
    incluir_graficos: bool = True
    incluir_comparaciones: bool = True
    formato_exportacion: FormatoReporte = FormatoReporte.PDF
    enviar_email: bool = False
    email_destinatarios: Optional[List[str]] = None
    programar_automatico: bool = False
    frecuencia_automatica: Optional[PeriodoReporte] = None


@strawberry.type
class MetadataReporte:
    """Metadatos del reporte generado"""
    id_reporte: str
    fecha_generacion: datetime
    usuario_solicitante: str
    tiempo_procesamiento: float
    total_registros: int
    filtros_aplicados: str  # JSON
    url_descarga: Optional[str] = None
    fecha_expiracion: Optional[datetime] = None


@strawberry.type
class ResumenReporte:
    """Resumen ejecutivo del reporte"""
    puntos_clave: List[str]
    tendencias_principales: List[str]
    alertas: List[str]
    recomendaciones: List[str]
    metricas_destacadas: List[str]  # JSON con métrica y valor


@strawberry.type
class ReporteCompleto:
    """Reporte completo con toda la información"""
    metadata: MetadataReporte
    resumen: ResumenReporte
    reporte_financiero: Optional[ReporteFinanciero] = None
    reporte_clinico: Optional[ReporteClinico] = None
    reporte_operacional: Optional[ReporteOperacional] = None
    reporte_inventario: Optional[ReporteInventario] = None
    reporte_cliente: Optional[ReporteCliente] = None
    reporte_mascota: Optional[ReporteMascota] = None
    reporte_comparativo: Optional[ReporteComparativo] = None
    reporte_predictivo: Optional[ReportePredictivo] = None
    graficos: Optional[List[str]] = None  # URLs o datos de gráficos