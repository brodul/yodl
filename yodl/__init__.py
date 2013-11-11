#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'


from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from yodl.models import DBSession
from yodl.models import SongItem


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    SongItem.metadata.create_all(engine)
    config = Configurator(
        settings=settings,
        session_factory=my_session_factory
    )
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('media', 'media', cache_max_age=3600)
    config.add_route('home', '/')
    config.include('pyramid_jinja2')
    config.scan()
    return config.make_wsgi_app()
