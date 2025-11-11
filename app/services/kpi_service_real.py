"""
Servicio de KPIs CORREGIDO basado en la estructura REAL de la base de datos
"""
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, func
from app.models.kpi_models import (
    DashboardResumen, CitasPorMes, MascotasPorEspecie,
    DoctorPerformance, VacunacionEstadisticas, AlertaVacunacion
)


class KPIServiceReal:
    """Servicio para obtener KPIs basado en la estructura REAL de la base de datos"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_dashboard_resumen(self) -> DashboardResumen:
        """Obtiene el resumen del dashboard basado en datos reales"""
        
        # Conteo de mascotas
        query_mascotas = text("SELECT COUNT(*) FROM mascota")
        resultado_mascotas = await self.db.execute(query_mascotas)
        total_mascotas = resultado_mascotas.scalar() or 0
        
        # Conteo de clientes
        query_clientes = text("SELECT COUNT(*) FROM cliente")
        resultado_clientes = await self.db.execute(query_clientes)
        total_clientes = resultado_clientes.scalar() or 0
        
        # Conteo de citas de hoy
        query_citas_hoy = text("""
            SELECT COUNT(*) 
            FROM cita 
            WHERE DATE(fechareserva) = CURRENT_DATE
        """)
        resultado_citas_hoy = await self.db.execute(query_citas_hoy)
        citas_hoy = resultado_citas_hoy.scalar() or 0
        
        # Total de citas en general
        query_total_citas = text("SELECT COUNT(*) FROM cita")
        resultado_total_citas = await self.db.execute(query_total_citas)
        total_citas = resultado_total_citas.scalar() or 0
        
        return DashboardResumen(
            total_mascotas=int(total_mascotas),
            total_clientes=int(total_clientes),
            total_citas=int(total_citas),
            citas_hoy=int(citas_hoy),
            ingresos_mes=0.0,  # No hay datos de precios en la BD real
            crecimiento_mensual=0.0  # No se puede calcular sin precios
        )
    
    async def get_citas_por_mes(self, anio: Optional[int] = None) -> List[CitasPorMes]:
        """Obtiene estadísticas de citas agrupadas por mes usando estructura real"""
        
        if anio is None:
            anio = datetime.now().year
        
        query = text("""
            SELECT 
                TO_CHAR(fechareserva, 'Month') as mes,
                EXTRACT(YEAR FROM fechareserva) as anio,
                COUNT(*) as total_citas,
                COUNT(CASE WHEN estado = 3 THEN 1 END) as citas_completadas,
                COUNT(CASE WHEN estado = 4 THEN 1 END) as citas_canceladas
            FROM cita
            WHERE EXTRACT(YEAR FROM fechareserva) = :anio
            GROUP BY 
                TO_CHAR(fechareserva, 'Month'),
                EXTRACT(YEAR FROM fechareserva),
                EXTRACT(MONTH FROM fechareserva)
            ORDER BY EXTRACT(MONTH FROM fechareserva)
        """)
        
        resultado = await self.db.execute(query, {'anio': anio})
        datos = resultado.fetchall()
        
        citas_por_mes = []
        for row in datos:
            total = row[2]
            completadas = row[3]
            tasa_completitud = (completadas / total * 100) if total > 0 else 0
            
            citas_por_mes.append(CitasPorMes(
                mes=str(row[0]).strip(),
                anio=int(row[1]),
                total_citas=int(total),
                citas_completadas=int(completadas),
                citas_canceladas=int(row[4]),
                tasa_completitud=round(tasa_completitud, 2)
            ))
        
        return citas_por_mes
    
    async def get_mascotas_por_especie(self) -> List[MascotasPorEspecie]:
        """Obtiene distribución de mascotas por especie usando estructura real"""
        
        query = text("""
            SELECT 
                e.descripcion as especie,
                COUNT(m.id) as total_mascotas,
                (COUNT(m.id) * 100.0 / (SELECT COUNT(*) FROM mascota)) as porcentaje
            FROM especie e
            LEFT JOIN mascota m ON e.id = m.especie_id
            GROUP BY e.id, e.descripcion
            ORDER BY total_mascotas DESC
        """)
        
        resultado = await self.db.execute(query)
        datos = resultado.fetchall()
        
        mascotas_por_especie = []
        for row in datos:
            mascotas_por_especie.append(MascotasPorEspecie(
                especie=str(row[0]),
                total_mascotas=int(row[1]),
                porcentaje=round(float(row[2]), 2)
            ))
        
        return mascotas_por_especie
    
    async def get_doctor_performance(
        self, 
        mes: Optional[int] = None, 
        anio: Optional[int] = None
    ) -> List[DoctorPerformance]:
        """Obtiene estadísticas de rendimiento por doctor usando estructura real"""
        
        if anio is None:
            anio = datetime.now().year
        if mes is None:
            mes = datetime.now().month
        
        query = text("""
            SELECT 
                d.id as doctor_id,
                CONCAT(d.nombre, ' ', d.apellido) as doctor_nombre,
                COUNT(c.id) as total_citas,
                COUNT(CASE WHEN c.estado = 3 THEN 1 END) as citas_completadas,
                COUNT(DISTINCT diag.id) as total_diagnosticos
            FROM doctor d
            LEFT JOIN cita c ON d.id = c.doctor_id
                AND EXTRACT(MONTH FROM c.fechareserva) = :mes
                AND EXTRACT(YEAR FROM c.fechareserva) = :anio
            LEFT JOIN diagnostico diag ON c.id = diag.cita_id
            GROUP BY d.id, d.nombre, d.apellido
            ORDER BY total_citas DESC
        """)
        
        resultado = await self.db.execute(query, {'mes': mes, 'anio': anio})
        datos = resultado.fetchall()
        
        performances = []
        for row in datos:
            total_citas = int(row[2])
            citas_completadas = int(row[3])
            total_diagnosticos = int(row[4])
            
            tasa_completitud = (citas_completadas / total_citas * 100) if total_citas > 0 else 0
            promedio_diagnosticos = (total_diagnosticos / citas_completadas) if citas_completadas > 0 else 0
            
            performances.append(DoctorPerformance(
                doctor_id=int(row[0]),
                doctor_nombre=str(row[1]),
                total_citas=total_citas,
                citas_completadas=citas_completadas,
                tasa_completitud=round(tasa_completitud, 2),
                promedio_diagnosticos_por_cita=round(promedio_diagnosticos, 2)
            ))
        
        return performances
    
    async def get_vacunacion_estadisticas(self) -> VacunacionEstadisticas:
        """Obtiene estadísticas de vacunación usando estructura real"""
        
        # Total de vacunaciones aplicadas
        query_total = text("""
            SELECT COUNT(*) 
            FROM detalle_vacunacion
        """)
        resultado_total = await self.db.execute(query_total)
        total_vacunaciones = resultado_total.scalar() or 0
        
        # Vacunaciones vencidas (próxima vacunación ya pasó)
        query_vencidas = text("""
            SELECT COUNT(*) 
            FROM detalle_vacunacion 
            WHERE proximavacunacion < CURRENT_DATE
        """)
        resultado_vencidas = await self.db.execute(query_vencidas)
        vacunaciones_vencidas = resultado_vencidas.scalar() or 0
        
        # Vacunaciones próximas (en los próximos 30 días)
        query_proximas = text("""
            SELECT COUNT(*) 
            FROM detalle_vacunacion 
            WHERE proximavacunacion BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
        """)
        resultado_proximas = await self.db.execute(query_proximas)
        vacunaciones_proximas = resultado_proximas.scalar() or 0
        
        # Vacunas más aplicadas
        query_mas_aplicadas = text("""
            SELECT v.descripcion, COUNT(dv.id) as total
            FROM vacuna v
            JOIN detalle_vacunacion dv ON v.id = dv.vacuna_id
            GROUP BY v.id, v.descripcion
            ORDER BY total DESC
            LIMIT 5
        """)
        resultado_mas_aplicadas = await self.db.execute(query_mas_aplicadas)
        datos_mas_aplicadas = resultado_mas_aplicadas.fetchall()
        
        vacunas_mas_aplicadas = [f"{row[0]} ({row[1]} aplicaciones)" for row in datos_mas_aplicadas]
        
        return VacunacionEstadisticas(
            total_vacunaciones=int(total_vacunaciones),
            vacunaciones_vencidas=int(vacunaciones_vencidas),
            vacunaciones_proximas=int(vacunaciones_proximas),
            vacunas_mas_aplicadas=vacunas_mas_aplicadas
        )
    
    async def get_alertas_vacunacion(self, dias_limite: int = 30) -> List[AlertaVacunacion]:
        """Obtiene alertas de vacunaciones próximas o vencidas usando estructura real"""
        
        query = text("""
            SELECT 
                m.id as mascota_id,
                m.nombre as mascota_nombre,
                CONCAT(c.nombre, ' ', c.apellido) as cliente_nombre,
                v.descripcion as vacuna,
                dv.fechavacunacion as fecha_ultima,
                dv.proximavacunacion as fecha_proxima,
                CASE 
                    WHEN dv.proximavacunacion < CURRENT_DATE 
                    THEN CURRENT_DATE - dv.proximavacunacion
                    ELSE dv.proximavacunacion - CURRENT_DATE
                END as dias_diferencia,
                CASE 
                    WHEN dv.proximavacunacion < CURRENT_DATE THEN 'VENCIDA'
                    WHEN dv.proximavacunacion <= CURRENT_DATE + INTERVAL '7 days' THEN 'URGENTE'
                    WHEN dv.proximavacunacion <= CURRENT_DATE + INTERVAL '30 days' THEN 'PRÓXIMA'
                    ELSE 'NORMAL'
                END as prioridad
            FROM detalle_vacunacion dv
            JOIN carnet_vacunacion cv ON dv.carnet_vacunacion_id = cv.id
            JOIN mascota m ON cv.mascota_id = m.id
            JOIN cliente c ON m.cliente_id = c.id
            JOIN vacuna v ON dv.vacuna_id = v.id
            WHERE dv.proximavacunacion <= CURRENT_DATE + INTERVAL ':dias_limite days'
                OR dv.proximavacunacion < CURRENT_DATE
            ORDER BY 
                CASE 
                    WHEN dv.proximavacunacion < CURRENT_DATE THEN 1
                    ELSE 2
                END,
                dv.proximavacunacion ASC
        """)
        
        resultado = await self.db.execute(query, {'dias_limite': dias_limite})
        datos = resultado.fetchall()
        
        alertas = []
        for row in datos:
            # Calcular días de vencimiento (negativo si está vencida)
            dias_vencimiento = int(row[6])
            if row[7] == 'VENCIDA':
                dias_vencimiento = -dias_vencimiento
            
            alertas.append(AlertaVacunacion(
                mascota_id=int(row[0]),
                mascota_nombre=str(row[1]),
                cliente_nombre=str(row[2]),
                tipo_vacuna=str(row[3]),
                fecha_ultima=str(row[4]) if row[4] else None,
                fecha_proxima=str(row[5]),
                dias_vencimiento=dias_vencimiento,
                prioridad=str(row[7])
            ))
        
        return alertas