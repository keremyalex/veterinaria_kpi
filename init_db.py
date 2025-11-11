"""
Script de inicialización del microservicio de KPIs
Compatible con Windows, Linux y macOS
"""
import asyncio
import sys
import os
from pathlib import Path

# Agregar el directorio app al path de manera compatible multiplataforma
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(app_dir))

try:
    from app.config.database import test_connection, engine
    from app.config.settings import settings
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("💡 Asegúrate de que las dependencias estén instaladas:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


async def init_database():
    """
    Inicializar la base de datos y crear vistas para KPIs
    """
    print("🔧 Inicializando base de datos para KPIs...")
    
    # Probar conexión
    if not await test_connection():
        print("❌ Error: No se puede conectar a la base de datos")
        return False
    
    print("✅ Conexión a base de datos establecida")
    
    try:
        # Crear tablas si no existen (aunque ya deberían existir)
        async with engine.begin() as conn:
            # En este caso, no creamos las tablas porque ya existen
            # Solo vamos a crear vistas útiles para KPIs
            
            # Vista para estadísticas mensuales de citas
            await conn.execute("""
                CREATE OR REPLACE VIEW vista_citas_mensuales AS
                SELECT 
                    EXTRACT(YEAR FROM fechareserva) as año,
                    EXTRACT(MONTH FROM fechareserva) as mes,
                    COUNT(*) as total_citas,
                    COUNT(CASE WHEN estado = 3 THEN 1 END) as citas_completadas,
                    COUNT(CASE WHEN estado = 4 THEN 1 END) as citas_canceladas,
                    ROUND(
                        COUNT(CASE WHEN estado = 3 THEN 1 END) * 100.0 / COUNT(*), 
                        2
                    ) as tasa_completitud
                FROM cita 
                GROUP BY 
                    EXTRACT(YEAR FROM fechareserva),
                    EXTRACT(MONTH FROM fechareserva)
                ORDER BY año DESC, mes DESC;
            """)
            
            # Vista para estadísticas de doctores
            await conn.execute("""
                CREATE OR REPLACE VIEW vista_doctor_performance AS
                SELECT 
                    d.id,
                    d.nombre || ' ' || d.apellido as doctor_nombre,
                    COUNT(c.id) as total_citas,
                    COUNT(CASE WHEN c.estado = 3 THEN 1 END) as citas_completadas,
                    ROUND(
                        COUNT(CASE WHEN c.estado = 3 THEN 1 END) * 100.0 / 
                        NULLIF(COUNT(c.id), 0), 
                        2
                    ) as tasa_completitud,
                    COALESCE(
                        (SELECT ROUND(AVG(diag_count), 2) 
                         FROM (
                             SELECT COUNT(diag.id) as diag_count
                             FROM cita c2 
                             LEFT JOIN diagnostico diag ON c2.id = diag.cita_id
                             WHERE c2.doctor_id = d.id
                             GROUP BY c2.id
                         ) subq),
                        0
                    ) as promedio_diagnosticos_por_cita
                FROM doctor d
                LEFT JOIN cita c ON d.id = c.doctor_id
                GROUP BY d.id, d.nombre, d.apellido
                HAVING COUNT(c.id) > 0;
            """)
            
            # Vista para vacunaciones próximas
            await conn.execute("""
                CREATE OR REPLACE VIEW vista_vacunaciones_proximas AS
                SELECT 
                    m.id as mascota_id,
                    m.nombre as mascota_nombre,
                    cl.nombre || ' ' || cl.apellido as cliente_nombre,
                    cl.telefono as cliente_telefono,
                    v.descripcion as vacuna,
                    dv.proximavacunacion,
                    CASE 
                        WHEN dv.proximavacunacion < CURRENT_DATE THEN 
                            CURRENT_DATE - dv.proximavacunacion
                        ELSE 0 
                    END as dias_vencida,
                    CASE 
                        WHEN dv.proximavacunacion < CURRENT_DATE THEN 'VENCIDA'
                        WHEN dv.proximavacunacion <= CURRENT_DATE + INTERVAL '7 days' THEN 'URGENTE'
                        WHEN dv.proximavacunacion <= CURRENT_DATE + INTERVAL '15 days' THEN 'PRÓXIMA'
                        ELSE 'PROGRAMADA'
                    END as urgencia
                FROM detalle_vacunacion dv
                JOIN carnet_vacunacion cv ON dv.carnet_vacunacion_id = cv.id
                JOIN mascota m ON cv.mascota_id = m.id
                JOIN cliente cl ON m.cliente_id = cl.id
                JOIN vacuna v ON dv.vacuna_id = v.id
                WHERE dv.proximavacunacion IS NOT NULL
                ORDER BY dv.proximavacunacion;
            """)
            
            # Índices para optimizar consultas de KPIs
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_cita_fecha_reserva 
                ON cita(fechareserva);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_cita_estado 
                ON cita(estado);
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_detalle_vacunacion_proxima 
                ON detalle_vacunacion(proximavacunacion);
            """)
            
            print("✅ Vistas y índices para KPIs creados correctamente")
            
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False
    
    return True


async def main():
    """Función principal"""
    print("🚀 Iniciando script de inicialización...")
    print(f"📊 Configuración: {settings.api_title}")
    print(f"🗄️  Base de datos: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")
    
    if await init_database():
        print("✅ Inicialización completada exitosamente")
        return 0
    else:
        print("❌ Error durante la inicialización")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())