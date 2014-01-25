# -*- coding: utf-8 -*-
"""Modelo para el Proyecto de Trackings de actividades."""

#from sqlalchemy.orm import relation
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Boolean, Date, Text
#from sqlalchemy.orm import relation, backref

#from tgtodotrack.model import DeclarativeBase, metadata, DBSession
from tgtodotrack.model import DeclarativeBase
from datetime import datetime


class Actividad(DeclarativeBase):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True)
    actividad = Column(Unicode(255), nullable=False)
    data = Column(Text, nullable=False)
    fecha = Column(Date, default=datetime.now)  # este timestamp por si no ponemos fecha
    public = Column(Boolean, default=False)  # Queremos filtrar actividades públicas de privadas
    user_id = Column(Integer, ForeignKey('tg_user.user_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
