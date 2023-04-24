from App.models import *
from App.database import db

def create_user(first_name, last_name, email, username, password):
    user = User.query.filter_by(username = username).first()
    if user: 
        return None
    
    user = User.query.filter_by(email = email).first()
    if user: 
        return None
    
    newuser = RegularUser(first_name = first_name, last_name = last_name, email = email, username=username, password=password)

    try: 
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except Exception:  # attempted to insert a duplicate user
        db.session.rollback()
        return None


def create_coordinator(first_name, last_name, email, username, password, organization_name):
 
    coordinator = Coordinator.query.filter_by(username = username).first()
    if coordinator: 
        return None
    
    coordinator = Coordinator.query.filter_by(email = email).first()
    if coordinator: 
        return None

    organization = Organization.query.filter_by(name = organization_name).first()
    
    if not organization:
        organization = Organization(name = organization_name)
        db.session.add(organization)
        db.session.commit()
        organization_id = organization.id
    else:
        organization_id = organization.id    

    newcoordinator = Coordinator(first_name = first_name, last_name = last_name, email = email, username=username, password=password, organization_id = organization_id)
    try:
        db.session.add(newcoordinator)
        db.session.commit()
        return newcoordinator
    except Exception as e: 
        db.session.rollback()
        return None
    

def get_all_users():
    return User.query.all()


def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users


def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


def get_user(username):
    return User.query.filter_by(username = username).first()

def get_coordinator(username):
    return Coordinator.query.filter_by(username = username).first()

def update_user(id, username):
    user = User.query.get(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
