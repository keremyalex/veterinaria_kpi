"""
Modelos de base de datos para el sistema de veterinaria
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime, date
from typing import Optional


class Doctor(Base):
    __tablename__ = "doctor"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    ci = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    fotourl = Column(String(255), nullable=True)
    
    # Relaciones
    citas = relationship("Cita", back_populates="doctor")


class Cliente(Base):
    __tablename__ = "cliente"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    ci = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(255), nullable=False)
    fotourl = Column(String(255), nullable=True)
    
    # Relaciones
    mascotas = relationship("Mascota", back_populates="cliente")


class Especie(Base):
    __tablename__ = "especie"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    
    # Relaciones
    mascotas = relationship("Mascota", back_populates="especie")


class Mascota(Base):
    __tablename__ = "mascota"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    fechanacimiento = Column(Date, nullable=False)
    raza = Column(String(255), nullable=False)
    sexo = Column(String(255), nullable=False)
    fotourl = Column(String(255), nullable=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    especie_id = Column(Integer, ForeignKey("especie.id"), nullable=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="mascotas")
    especie = relationship("Especie", back_populates="mascotas")
    citas = relationship("Cita", back_populates="mascota")
    carnet_vacunacion = relationship("CarnetVacunacion", back_populates="mascota", uselist=False)


class BloqueHorario(Base):
    __tablename__ = "bloque_horario"
    
    id = Column(Integer, primary_key=True, index=True)
    diasemana = Column(Integer, nullable=False)
    horainicio = Column(Time, nullable=False)
    horafinal = Column(Time, nullable=False)
    activo = Column(Integer, nullable=False)
    
    # Relaciones
    citas = relationship("Cita", back_populates="bloque_horario")


class Cita(Base):
    __tablename__ = "cita"
    
    id = Column(Integer, primary_key=True, index=True)
    fechacreacion = Column(DateTime, nullable=False)
    motivo = Column(String(255), nullable=False)
    fechareserva = Column(DateTime, nullable=False)
    estado = Column(Integer, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascota.id"), nullable=False)
    bloque_horario_id = Column(Integer, ForeignKey("bloque_horario.id"), nullable=True)
    
    # Relaciones
    doctor = relationship("Doctor", back_populates="citas")
    mascota = relationship("Mascota", back_populates="citas")
    bloque_horario = relationship("BloqueHorario", back_populates="citas")
    diagnosticos = relationship("Diagnostico", back_populates="cita")


class Diagnostico(Base):
    __tablename__ = "diagnostico"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    fecharegistro = Column(DateTime, nullable=False)
    observaciones = Column(String(255), nullable=False)
    cita_id = Column(Integer, ForeignKey("cita.id"), nullable=False)
    
    # Relaciones
    cita = relationship("Cita", back_populates="diagnosticos")
    tratamientos = relationship("Tratamiento", back_populates="diagnostico")


class Tratamiento(Base):
    __tablename__ = "tratamiento"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
    observaciones = Column(String(255), nullable=False)
    diagnostico_id = Column(Integer, ForeignKey("diagnostico.id"), nullable=False)
    
    # Relaciones
    diagnostico = relationship("Diagnostico", back_populates="tratamientos")


class Vacuna(Base):
    __tablename__ = "vacuna"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    
    # Relaciones
    detalles_vacunacion = relationship("DetalleVacunacion", back_populates="vacuna")


class CarnetVacunacion(Base):
    __tablename__ = "carnet_vacunacion"
    
    id = Column(Integer, primary_key=True, index=True)
    fechaemision = Column(DateTime, nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascota.id"), nullable=False, unique=True)
    
    # Relaciones
    mascota = relationship("Mascota", back_populates="carnet_vacunacion")
    detalles_vacunacion = relationship("DetalleVacunacion", back_populates="carnet_vacunacion")


class DetalleVacunacion(Base):
    __tablename__ = "detalle_vacunacion"
    
    id = Column(Integer, primary_key=True, index=True)
    fechavacunacion = Column(Date, nullable=False)
    proximavacunacion = Column(Date, nullable=True)
    carnet_vacunacion_id = Column(Integer, ForeignKey("carnet_vacunacion.id"), nullable=False)
    vacuna_id = Column(Integer, ForeignKey("vacuna.id"), nullable=False)
    
    # Relaciones
    carnet_vacunacion = relationship("CarnetVacunacion", back_populates="detalles_vacunacion")
    vacuna = relationship("Vacuna", back_populates="detalles_vacunacion")