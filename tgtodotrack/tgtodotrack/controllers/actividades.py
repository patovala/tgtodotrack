# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose, require, request
#from tg import redirect, validate, flash
from tg import redirect, flash

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import authorize

# project specific imports
from tgtodotrack.lib.base import BaseController
from repoze.what.predicates import in_group
#from tgtodotrack.model import DBSession, metadata
from tgtodotrack.model import DBSession
from tgtodotrack.model.modelo import Actividad
from tgtodotrack.model.auth import User
from datetime import datetime


class Actividades(BaseController):
    allow_only = authorize.not_anonymous()

    @expose('tgtodotrack.templates.actividades.intro')
    def index(self, **kw):
        user_name = request.identity['repoze.who.userid']
        fecha = datetime.now().date()
        user = DBSession.query(User).filter_by(user_name=user_name).first()
        actividades = DBSession.query(Actividad).filter_by(fecha=fecha, public=True).all()
        misactividades = DBSession.query(Actividad).filter_by(usuario=user).all()
        return dict(actividades=actividades, fecha=fecha, usuario=user, misactividades=misactividades)

    #PV - Step15 - controles de acceso por controlador
    @expose('tgtodotrack.templates.actividades.intro')
    @require(in_group('trabajadores', msg=u'Acceso exclusivo del grupo trabajadores'))
    def crear_actividad(self, **kw):
        """Lista las citas de un paciente con opcion a crear"""
        # Obtener el usuario que ingresó al sistema
        user_name = request.identity['repoze.who.userid']
        user = DBSession.query(User).filter_by(user_name=user_name).first()

        if (kw['fecha'] != ""):
            fecha = datetime.strptime(kw['fecha'], '%m/%d/%Y')
        else:
            fecha = None

        actividad = Actividad(data=kw['data'], actividad=kw['actividad'], usuario=user)
        if fecha:
            actividad.fecha = fecha

        if kw['public'] == u"si":
            actividad.public = True

        DBSession.add(actividad)
        flash("Actividad Creada")
        redirect("/actividades/")
