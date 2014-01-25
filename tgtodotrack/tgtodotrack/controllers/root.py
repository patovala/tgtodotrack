# -*- coding: utf-8 -*-
"""Main Controller"""

#from tg import expose, flash, require, url, lurl, request, redirect
from tg import expose, flash, require, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgtodotrack import model
from repoze.what import predicates
#from tgtodotrack.controllers.secure import SecureController
#from tgtodotrack.model import DBSession, metadata
from tgtodotrack.model import DBSession
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from tgtodotrack.lib.base import BaseController
from tgtodotrack.controllers.error import ErrorController
# PV Step04 - cargar el controlador para poder publicarlo en el root
from tgtodotrack.controllers.actividades import Actividades

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the tgtodotrack application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    #secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    actividades = Actividades()

    @expose('tgtodotrack.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('tgtodotrack.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('tgtodotrack.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('tgtodotrack.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('tgtodotrack.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('tgtodotrack.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('tgtodotrack.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('tgtodotrack.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Credenciales Incorrectas'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/actividades/',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        # RZ - Step18 - Arreglar internacionalización simple
        flash(_('Bienvenido, %s!') % userid)
        if (userid == u"manager"):
            redirect('/admin')
        else:
            redirect('/actividades/')
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Esperamos verlos pronto!'))
        redirect(came_from)
