import transaction, datetime

from sqlalchemy import Column, Integer, Unicode, Date, ForeignKey
from sqlalchemy import DateTime, String, Boolean, UnicodeText

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


from pyramid.security import Allow
from pyramid.security import Everyone

class RootFactory(object):
    __acl__ = [ (Allow, 'group:users', 'logged_in'),
                (Allow, 'group:admins', 'logged_in'),
                (Allow, 'group:admins', 'administrative') ]
    def __init__(self, request):
        pass

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256))
    birthday = Column(Date)
    password = Column(String(128))
    email = Column(Unicode(512))
    active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    items = relationship('Item', backref="owner")
    
    def __init__(self, name, email, password, birthday=None, active=True, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.birthday = birthday
        self.active = active
        self.is_admin = is_admin

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512))
    description = Column(UnicodeText)
    owner_id = Column(Integer, ForeignKey('people.id'))
    url = Column(Unicode(1024))
    multiple = Column(Boolean)
    marked = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    created_on = Column(DateTime)
    deleted_on = Column(DateTime)
    marked_on = Column(DateTime)
    

    def __init__(self, title, description, owner_id, url=None, multiple=False):
        self.title = title
        self.description = description
        self.url = url
        self.multiple = multiple
        self.marked = 0
        self.active = True
        self.deleted = False
        self.owner_id = owner_id
        self.created_on = datetime.datetime.now()

def populate():
    session = DBSession()
    jon = DBSession.query(Person).filter(Person.email==u'jon@craftyjon.com').first()
    if jon is None:
        jon = Person(u'Jon Evans', u'jon@craftyjon.com', '3b9e1cec984aa5d85732a14bbac2a737ef8b1ecf0d30828da2862f11', is_admin=True)
        session.add(jon)
        session.flush()
        transaction.commit()
        test_item = Item(u'Test Item', u'Test Description')
        test_item.owner = jon
        session.add(test_item)
        session.flush()
        transaction.commit()
        test_item = Item(u'Another', u'Another Description')
        test_item.owner = jon
        session.add(test_item)
        session.flush()
        transaction.commit()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        transaction.abort()
