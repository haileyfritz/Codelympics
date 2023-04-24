from App.database import db

class TeamMember(db.Model):
    __tablename__ = 'team_member'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, unique = False)


    def get_json(self):
        return{
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id
        }


    def repr(self):
        return f'<Team Member {self.id} : {self.team_id.team_name} - {self.user_id.username}>'