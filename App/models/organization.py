
from App.models import Competition
# from App.models import Coordinator
from App.database import db

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(80), nullable = False)
    #coordinators = db.relationship('Coordinator', backref = 'coordinator', lazy = True)
    competitions = db.relationship('Competition', backref = 'competition', lazy = True)
    

    def __init__(self, name):
        self.name = name


    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
        }


    def repr(self):
        return f'<Organization {self.id}: {self.name}>' 