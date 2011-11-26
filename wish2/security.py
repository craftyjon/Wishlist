from wish2.models import DBSession, Person

def groupfinder(id, request):
    dbuser = DBSession.query(Person).filter(Person.id==id).first()
    if dbuser is not None:
        if dbuser.is_admin:
            return ['group:admins']
        else:
            return ['group:users']
