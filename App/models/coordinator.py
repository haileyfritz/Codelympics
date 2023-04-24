from sqlalchemy.sql.expression import func
from App.models import *
from App.database import db

class Coordinator(User):
    __tablename__ = 'coordinator'
    coordinator_id = db.Column(db.Integer,  primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __init__(self, organization_id, first_name, last_name, email, username, password):
        super().__init__(first_name, last_name, email, username, password)
        self.organization_id = organization_id



    def add_competition(self, competition_name, start_time, end_time):
        competition = Competition.query.filter_by(name = competition_name).first()
        if competition:
            return None

        new_competition = Competition(name = competition_name, organization_id = self.organization_id, start_time = start_time, end_time = end_time)

        organization = Organization.query.get(self.organization_id)
        organization.competitions.append(new_competition)

        db.session.add(new_competition)
        db.session.commit()
        return new_competition


    def edit_competition(self, competition_id, competition_name, start_time, end_time):
        competition = Competition.query.get(competition_id)
        if competition.organization_id == self.organization_id:
            competition.name = competition_name
            competition.start_time = start_time
            competition.end_time = end_time
            competition.organization_id = self.organization_id
            
            db.session.add(competition)
            db.session.commit()
            return competition
        return None


    def remove_competition(self, competition_id):
        competition = Competition.query.get(competition_id)
        if not competition:
            return None
        
        if competition.organization_id == self.organization_id:
            db.session.delete(competition)
            db.session.commit()
            return True
        return None


    def add_team(self, competition_id, team_name, points, time_taken):
        team = Team.query.filter_by(team_name = team_name).first()
        if team:
            return None

        new_team = Team(competition_id, team_name, points, time_taken)
        competition = Competition.query.get(competition_id)
        competition.teams.append(new_team)
        db.session.add(new_team)
        db.session.commit()
        return new_team


    def edit_team(self, competition_id, team_id, team_name, points, time_taken):
        
        team = Team.query.get(team_id)
        if team:
            team.competition_id = competition_id
            team.team_name = team_name
            team.points = points
            team.time_taken = time_taken

            db.session.add(team)
            db.session.commit()
            return team
        return None


    def remove_team(self, team_id):
        team = Team.query.get(team_id)
        if not team:
            return None
        
        db.session.delete(team)
        db.session.commit()
        return True



    def add_team_member(self, team_id, username):
        team = Team.query.get(team_id)
        print(team)
        if not team:
            return None
        
        user = User.query.filter_by(username = username).first()
        print(user)
        if not user:
            return None
        
        team.members.append(user)
        db.session.commit()
        return True



    def remove_team_member(self, team_id, username):
        team = Team.query.get(team_id)
        if not team:
            return None
        
        user = User.query.filter_by(username = username).first()
        if not user:
            return None
        
        team.members.remove(user)
        db.session.commit()
        return True


    def get_json(self):
        return{
            'coordinator_id': self.coordinator_id,
            'organization_id': self.organization_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username
        }

    def repr(self):
        return f'<Coordinator {self.coordinator_id} : {self.first_name} {self.last_name} {self.username} - {self.email}>'  