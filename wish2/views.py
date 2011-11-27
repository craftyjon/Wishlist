from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound

from wish2.models import DBSession
from wish2.models import Person, Item

import hashlib, datetime

def wish_render(request, response_dict):
    logged_in = authenticated_userid(request)
    dbsession = DBSession()
    is_admin = False
    current_user = None
    if logged_in:
        current_user = DBSession.query(Person).filter(Person.id==logged_in).first()
        if current_user:
            is_admin = current_user.is_admin
        
    response_dict['current_user'] = current_user
    response_dict['logged_in'] = logged_in
    response_dict['is_admin'] = is_admin
    return response_dict

def all_items(request):
    my_id = authenticated_userid(request)
    people = DBSession.query(Person).filter(Person.active==True).filter(Person.id!=my_id)
    return wish_render(request, {'people':people})
    
def people(request):
    my_id = authenticated_userid(request)
    people = DBSession.query(Person).filter(Person.active==True).filter(Person.id!=my_id)
    return wish_render(request, {'people':people})
    
def list(request):
    id = request.matchdict['id']
    person = DBSession.query(Person).filter(Person.id==id).first()
    if person.email==authenticated_userid(request):
        return HTTPFound(location = request.route_url('my_list'))
    return wish_render(request, {'person':person})
    
def my_list(request):
    id = authenticated_userid(request)
    person = DBSession.query(Person).filter(Person.id==id).first()
    return wish_render(request, {'person':person})
    
def profile(request):
    id = request.matchdict['id']
    person = DBSession.query(Person).filter(Person.id==id).first()
    return wish_render(request, {'person':person})
    
def edit_profile(request):
    id = authenticated_userid(request)
    if 'form.submitted' in request.params:
        person = DBSession.query(Person).filter(Person.id==id).one()
        person.name = request.params['name']
        person.email = request.params['email']
        if 'password' in request.params and request.params['password'] != "":
            new_password = hashlib.sha224(request.params['password']).hexdigest()
            person.password = new_password
        DBSession.add(person)
        return HTTPFound(location = request.route_url('edit_users'))
    save_url = request.route_url('edit_profile')
    person = DBSession.query(Person).filter(Person.id==id).first()
    return wish_render(request, dict(person=person, save_url=save_url))

def create_user(request):
    if 'form.submitted' in request.params:
        session = DBSession()
        name = request.params['name']
        email = request.params['email']
        password = hashlib.sha224(request.params['password']).hexdigest()
        person = Person(name, email, password)
        session.add(person)
        return HTTPFound(location = request.route_url('edit_users'))
    save_url = request.route_url('create_user')
    person = Person('', '', '')
    return wish_render(request, dict(person=person, save_url=save_url))
    
def edit_users(request):
    people = DBSession.query(Person)
    return wish_render(request, {'people':people})
    
def edit_user(request):
    id = request.matchdict['id']
    if 'form.submitted' in request.params:
        person = DBSession.query(Person).filter(Person.id==id).one()
        if 'delete' in request.params and request.params['delete']=="yes":
            DBSession.delete(person)
        else:
            person.name = request.params['name']
            person.email = request.params['email']
            if 'password' in request.params and request.params['password'] != "":
                new_password = hashlib.sha224(request.params['password']).hexdigest()
                person.password = new_password
            DBSession.add(person)
        return HTTPFound(location = request.route_url('edit_users'))
    save_url = request.route_url('edit_user', id=id)
    person = DBSession.query(Person).filter(Person.id==id).first()
    return wish_render(request, dict(person=person, save_url=save_url))

def view(request):
    id = request.matchdict['id']
    item = DBSession.query(Item).filter(Item.id==id).one()
    formatted_description = item.description.replace('\n','<br/>\n')
    return wish_render(request, {'item':item, 'formatted_description':formatted_description})
    
def mark(request):
    id = request.matchdict['id']
    item = DBSession.query(Item).filter(Item.id==id).one()
    if item.owner.email == authenticated_userid(request):
        return HTTPFound(location = request.route_url('my_list'))
    if 'form.submitted' in request.params:
        item.marked = item.marked + 1
        DBSession.add(item)
        return HTTPFound(location = request.route_url('list', id=item.owner_id))
    save_url = request.route_url('mark',id=id)
    return wish_render(request, dict(item=item, save_url=save_url))
    
def add(request):
    owner_id = authenticated_userid(request)
    if 'form.submitted' in request.params:
        session = DBSession()
        title = request.params['title']
        description = request.params['description']
        multiple = False
        if 'multiple' in request.params and request.params['multiple']=="True":
            multiple = True
        url = request.params['url'] or None
        item = Item(title, description, url=url, owner_id=owner_id, multiple=multiple)
        session.add(item)
        return HTTPFound(location = request.route_url('my_list'))
    save_url = request.route_url('add')
    item = Item('', '', '')
    return wish_render(request, dict(item=item, save_url=save_url))
    
def edit(request):
    id = request.matchdict['id']
    owner_id = authenticated_userid(request)
    if 'form.submitted' in request.params:
        item = DBSession.query(Item).filter(Item.id==id).one()
        if 'delete' in request.params and request.params['delete']=="yes":
            DBSession.delete(item)
        else:
            item.title = request.params['title']
            item.url = request.params['url']
            item.multiple = False
            if 'multiple' in request.params and request.params['multiple']=="True":
                print "Setting multiple to True"
                item.multiple = True
            item.description = request.params['description']
            DBSession.add(item)
        return HTTPFound(location = request.route_url('my_list'))
    save_url = request.route_url('edit', id=id)
    item = DBSession.query(Item).filter(Item.id==id).one()
    return wish_render(request, dict(item=item, save_url=save_url))
