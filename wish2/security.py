from wish2.models import DBSession, Person

def groupfinder(email, request):
    dbuser = DBSession.query(Person).filter(Person.email==email).first()
    if dbuser is not None:
        if dbuser.is_admin:
            return ['group:admins']
        else:
            return ['group:users']
