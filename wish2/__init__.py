from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from wish2.models import initialize_sql
from wish2.security import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'A(jn342kiZksdfoA4ijal3a4fi8a34njl#$9ia', callback=groupfinder, debug=False)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='wish2.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_static_view('static', 'wish2:static', cache_max_age=3600)
    
    config.add_route('all_items', '/')
    config.add_route('people', '/people')
    config.add_route('my_list', '/list/my')
    config.add_route('list', '/list/{id}')
    config.add_route('edit_profile', '/profile/edit')
    config.add_route('profile', '/profile/{id}')
    config.add_route('view', '/view/{id}')
    config.add_route('mark', '/mark/{id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{id}')
    config.add_route('create_user', '/create_user')
    config.add_route('edit_user', '/edit_user/{id}')
    config.add_route('edit_users', '/edit_users')
    
    config.add_view('wish2.views.all_items',
                    route_name='all_items',
                    renderer='templates/all_items.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.people',
                    route_name='people',
                    renderer='templates/people.pt',
                    permission='logged_in')
    
    config.add_view('wish2.views.list',
                    route_name='list',
                    renderer='templates/list.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.my_list',
                    route_name='my_list',
                    renderer='templates/my_list.pt',
                    permission='logged_in')
    
    config.add_view('wish2.views.profile',
                    route_name='profile',
                    renderer='templates/profile.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.view',
                    route_name='view',
                    renderer='templates/view.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.mark',
                    route_name='mark',
                    renderer='templates/mark.pt',
                    permission='logged_in')
    
    config.add_view('wish2.login.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='templates/login.pt')
    
    config.add_view('wish2.login.login',
                    route_name='login',
                    renderer='templates/login.pt')
    
    config.add_view('wish2.login.logout',
                    route_name='logout')
                    
    config.add_view('wish2.views.add',
                    route_name='add',
                    renderer='templates/add.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.edit',
                    route_name='edit',
                    renderer='templates/edit.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.edit_profile',
                    route_name='edit_profile',
                    renderer='templates/edit_profile.pt',
                    permission='logged_in')
                    
    config.add_view('wish2.views.create_user',
                    route_name='create_user',
                    renderer='templates/create_user.pt',
                    permission='administrative')
                    
    config.add_view('wish2.views.edit_user',
                    route_name='edit_user',
                    renderer='templates/edit_user.pt',
                    permission='administrative')
                    
    config.add_view('wish2.views.edit_users',
                    route_name='edit_users',
                    renderer='templates/edit_users.pt',
                    permission='administrative')
    
    return config.make_wsgi_app()

