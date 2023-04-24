from App.models import *
from App.database import db

def get_all_organizations():
    return Organization.query.all()

def get_all_organizations_json():
    orgs = Organization.query.all()
    if not orgs:
        return []
    orgs = [org.get_json() for org in orgs]
    return orgs