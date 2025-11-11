"""
Servicios para cálculo de KPIs
"""
from sqlalchemy import func, text, and_, or_, case, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
import calendar
from app.models.database_models import (
    Cita, Doctor, Cliente, Mascota, Especie, 
    Diagnostico, DetalleVacunacion, CarnetVacunacion, Vacuna
)
from app.models.kpi_models import (
    CitasPorMes, MascotasPorEspecie, DoctorPerformance,
    VacunacionEstadisticas, MascotasEstadisticas, TendenciasMensuales,
    AlertaVacunacion, DashboardResumen, KPIDetallado, GraficoData
)


class KPIService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_citas_por_mes(self, anio: Optional[int] = None) -> List[CitasPorMes]:
        """Obtiene estadísticas de citas agrupadas por mes"""
        if anio is None:
            anio = datetime.now().year

        query = select(
            extract('month', Cita.fechareserva).label('mes'),
            extract('year', Cita.fechareserva).label('anio'),
            func.count(Cita.id).label('total_citas'),
            func.sum(case((Cita.estado == 3, 1), else_=0)).label('citas_completadas'),
            func.sum(case((Cita.estado == 4, 1), else_=0)).label('citas_canceladas')
        ).where(
            extract('year', Cita.fechareserva) == anio
        ).group_by(
            extract('month', Cita.fechareserva),
            extract('year', Cita.fechareserva)
        ).order_by(
            extract('month', Cita.fechareserva)
        )

        result = await self.db.execute(query)
        rows = result.all()

        kpis = []
        for row in rows:
            tasa_completitud = (row.citas_completadas / row.total_citas * 100) if row.total_citas > 0 else 0
            mes_nombre = calendar.month_name[int(row.mes)]
            
            kpis.append(CitasPorMes(
                mes=mes_nombre,
                anio=int(row.anio),
                total_citas=row.total_citas,
                citas_completadas=row.citas_completadas,
                citas_canceladas=row.citas_canceladas,
                tasa_completitud=round(tasa_completitud, 2)
            ))

        return kpis

    async def get_mascotas_por_especie(self) -> List[MascotasPorEspecie]:
        """Obtiene estadísticas de mascotas agrupadas por especie"""
        # Primero obtenemos el total de mascotas
        total_query = select(func.count(Mascota.id))
        total_result = await self.db.execute(total_query)
        total_mascotas = total_result.scalar()

        # Luego obtenemos la distribución por especie
        query = select(
            Especie.descripcion.label('especie'),
            func.count(Mascota.id).label('total')
        ).select_from(
            Mascota.__table__.join(Especie.__table__)
        ).group_by(
            Especie.descripcion
        ).order_by(
            func.count(Mascota.id).desc()
        )

        result = await self.db.execute(query)
        rows = result.all()

        kpis = []
        for row in rows:
            porcentaje = (row.total / total_mascotas * 100) if total_mascotas > 0 else 0
            kpis.append(MascotasPorEspecie(
                especie=row.especie,
                total_mascotas=row.total,
                porcentaje=round(porcentaje, 2)
            ))

        return kpis

    async def get_doctor_performance(self, mes: Optional[int] = None, anio: Optional[int] = None) -> List[DoctorPerformance]:
        """Obtiene estadísticas de rendimiento por doctor"""
        if mes is None:
            mes = datetime.now().month
        if anio is None:
            anio = datetime.now().year

        query = select(
            Doctor.id,
            func.concat(Doctor.nombre, ' ', Doctor.apellido).label('doctor_nombre'),
            func.count(Cita.id).label('total_citas'),
            func.sum(case((Cita.estado == 3, 1), else_=0)).label('citas_completadas'),
            func.avg(
                select(func.count(Diagnostico.id))
                .select_from(Diagnostico)
                .where(Diagnostico.cita_id == Cita.id)
            ).label('promedio_diagnosticos')
        ).select_from(
            Doctor.__table__.outerjoin(Cita.__table__)
        ).where(
            and_(
                extract('month', Cita.fechareserva) == mes,
                extract('year', Cita.fechareserva) == anio
            )
        ).group_by(
            Doctor.id, Doctor.nombre, Doctor.apellido
        ).having(
            func.count(Cita.id) > 0
        )

        result = await self.db.execute(query)
        rows = result.all()

        kpis = []
        for row in rows:
            tasa_completitud = (row.citas_completadas / row.total_citas * 100) if row.total_citas > 0 else 0
            promedio_diagnosticos = row.promedio_diagnosticos or 0

            kpis.append(DoctorPerformance(
                doctor_id=row.id,
                doctor_nombre=row.doctor_nombre,
                total_citas=row.total_citas,
                citas_completadas=row.citas_completadas,
                tasa_completitud=round(tasa_completitud, 2),
                promedio_diagnosticos_por_cita=round(promedio_diagnosticos, 2)
            ))

        return kpis

    async def get_vacunacion_estadisticas(self) -> VacunacionEstadisticas:
        """Obtiene estadísticas de vacunación"""
        hoy = date.today()
        
        # Total vacunaciones
        total_query = select(func.count(DetalleVacunacion.id))
        total_result = await self.db.execute(total_query)
        total_vacunaciones = total_result.scalar()

        # Vacunaciones vencidas
        vencidas_query = select(func.count(DetalleVacunacion.id)).where(
            and_(
                DetalleVacunacion.proximavacunacion.isnot(None),
                DetalleVacunacion.proximavacunacion < hoy
            )
        )
        vencidas_result = await self.db.execute(vencidas_query)
        vacunaciones_vencidas = vencidas_result.scalar()

        # Vacunaciones próximas (próximos 30 días)
        proximas_query = select(func.count(DetalleVacunacion.id)).where(
            and_(
                DetalleVacunacion.proximavacunacion.isnot(None),
                DetalleVacunacion.proximavacunacion >= hoy,
                DetalleVacunacion.proximavacunacion <= hoy + timedelta(days=30)
            )
        )
        proximas_result = await self.db.execute(proximas_query)
        vacunaciones_proximas = proximas_result.scalar()

        # Vacunas más aplicadas
        vacunas_query = select(
            Vacuna.descripcion,
            func.count(DetalleVacunacion.id).label('total')
        ).select_from(
            DetalleVacunacion.__table__.join(Vacuna.__table__)
        ).group_by(
            Vacuna.descripcion
        ).order_by(
            func.count(DetalleVacunacion.id).desc()
        ).limit(5)

        vacunas_result = await self.db.execute(vacunas_query)
        vacunas_mas_aplicadas = [row.descripcion for row in vacunas_result.all()]

        return VacunacionEstadisticas(
            total_vacunaciones=total_vacunaciones,
            vacunaciones_vencidas=vacunaciones_vencidas,
            vacunaciones_proximas=vacunaciones_proximas,
            vacunas_mas_aplicadas=vacunas_mas_aplicadas
        )

    async def get_dashboard_resumen(self) -> DashboardResumen:
        """Obtiene resumen principal para el dashboard"""
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_mes = hoy.replace(day=1)

        # Total de mascotas
        mascotas_query = select(func.count(Mascota.id))
        mascotas_result = await self.db.execute(mascotas_query)
        total_mascotas = mascotas_result.scalar()

        # Total de clientes
        clientes_query = select(func.count(Cliente.id))
        clientes_result = await self.db.execute(clientes_query)
        total_clientes = clientes_result.scalar()

        # Total de doctores
        doctores_query = select(func.count(Doctor.id))
        doctores_result = await self.db.execute(doctores_query)
        total_doctores = doctores_result.scalar()

        # Citas de hoy
        citas_hoy_query = select(func.count(Cita.id)).where(
            func.date(Cita.fechareserva) == hoy
        )
        citas_hoy_result = await self.db.execute(citas_hoy_query)
        citas_hoy = citas_hoy_result.scalar()

        # Citas de la semana
        citas_semana_query = select(func.count(Cita.id)).where(
            func.date(Cita.fechareserva) >= inicio_semana
        )
        citas_semana_result = await self.db.execute(citas_semana_query)
        citas_semana = citas_semana_result.scalar()

        # Vacunaciones vencidas
        vencidas_query = select(func.count(DetalleVacunacion.id)).where(
            and_(
                DetalleVacunacion.proximavacunacion.isnot(None),
                DetalleVacunacion.proximavacunacion < hoy
            )
        )
        vencidas_result = await self.db.execute(vencidas_query)
        vacunaciones_vencidas = vencidas_result.scalar()

        # Nuevos clientes este mes
        nuevos_clientes_query = select(func.count(Cliente.id))
        # Nota: Necesitaríamos un campo fecha_registro en Cliente para esto
        # Por ahora asumimos 0
        nuevos_clientes_mes = 0

        # Tasa de ocupación (simplificada)
        # Asumiendo 8 horas laborables por día, 30 min por cita promedio
        citas_posibles_dia = 16  # 8 horas * 2 citas por hora
        tasa_ocupacion = (citas_hoy / citas_posibles_dia * 100) if citas_posibles_dia > 0 else 0

        return DashboardResumen(
            total_mascotas=total_mascotas,
            total_clientes=total_clientes,
            total_doctores=total_doctores,
            citas_hoy=citas_hoy,
            citas_semana=citas_semana,
            vacunaciones_vencidas=vacunaciones_vencidas,
            nuevos_clientes_mes=nuevos_clientes_mes,
            tasa_ocupacion=round(tasa_ocupacion, 2)
        )

    async def get_alertas_vacunacion(self, dias_limite: int = 30) -> List[AlertaVacunacion]:
        """Obtiene alertas de vacunaciones próximas o vencidas"""
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=dias_limite)

        query = select(
            Mascota.id,
            Mascota.nombre,
            func.concat(Cliente.nombre, ' ', Cliente.apellido).label('cliente_nombre'),
            Cliente.telefono,
            Vacuna.descripcion,
            DetalleVacunacion.proximavacunacion
        ).select_from(
            DetalleVacunacion.__table__
            .join(CarnetVacunacion.__table__)
            .join(Mascota.__table__)
            .join(Cliente.__table__)
            .join(Vacuna.__table__)
        ).where(
            and_(
                DetalleVacunacion.proximavacunacion.isnot(None),
                DetalleVacunacion.proximavacunacion <= fecha_limite
            )
        ).order_by(DetalleVacunacion.proximavacunacion)

        result = await self.db.execute(query)
        rows = result.all()

        alertas = []
        for row in rows:
            dias_diferencia = (row.proximavacunacion - hoy).days
            
            if dias_diferencia < 0:
                urgencia = "VENCIDA"
                dias_vencida = abs(dias_diferencia)
            elif dias_diferencia <= 7:
                urgencia = "URGENTE"
                dias_vencida = 0
            elif dias_diferencia <= 15:
                urgencia = "PRÓXIMA"
                dias_vencida = 0
            else:
                urgencia = "PROGRAMADA"
                dias_vencida = 0

            alertas.append(AlertaVacunacion(
                mascota_id=row.id,
                mascota_nombre=row.nombre,
                cliente_nombre=row.cliente_nombre,
                cliente_telefono=row.telefono,
                vacuna=row.descripcion,
                fecha_vencimiento=row.proximavacunacion,
                dias_vencida=dias_vencida,
                urgencia=urgencia
            ))

        return alertas