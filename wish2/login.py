from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import authenticated_userid

from wish2.models import DBSession, Person
import hashlib
import datetime

def login(request):
    logged_in = authenticated_userid(request)
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    email = ''
    password = ''
    is_admin = False
    if 'form.submitted' in request.params:
        email = request.params['email']
        password = request.params['password']
        hashpass = hashlib.sha224(str(password)).hexdigest()
        dbuser = DBSession.query(Person).filter(Person.email==email).first()
        if dbuser and dbuser.password == hashpass:
            print email+" successfully logged in on "+str(datetime.datetime.now())
            headers = remember(request, email)
            return HTTPFound(location = came_from,
                             headers = headers)
        else:
            print "Failed login attempt by "+email+" on "+str(datetime.datetime.now())
            print "db = "+dbuser.password
            print "given = "+hashpass
        message = 'Sorry, that login doesn\'t seem to work.  Try again?'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        email = email,
        password = password,
        logged_in = logged_in,
        is_admin = is_admin,
        )
    
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('login'),
                     headers = headers)
