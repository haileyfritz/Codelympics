from App.models import *
from App.database import db
from datetime import datetime, time

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable = False, unique = False)
    team_name = db.Column(db.String, nullable = False, unique = True)
    points = db.Column(db.Integer, unique = False, nullable = False)
    time_taken = db.Column(db.String, unique = False, nullable = True)
    rank = db.Column(db.Integer, unique = False)
    members = db.relationship('User', secondary = 'team_member', backref = 'team', lazy = True)


    def __init__(self, competition_id, team_name, points, time_taken):
        self.competition_id = competition_id
        self.team_name = team_name
        self.points = points
        self.time_taken = time_taken
        self.rank = 0


    def calculate_rank(self, teams, competition, points, time_taken):
        time_obj = datetime.strptime(time_taken, "%H:%M").time()

        rank = 1
        for t in teams:
            if t.points > points:
                rank = rank + 1
            elif t.points == points:
                t_time = t.time_taken
                t_time_obj = datetime.strptime(t_time, "%H:%M").time()

                if time_obj > t_time_obj:
                    rank = rank + 1
        
        #entry = LeaderBoard(competition.id, self.id, self.team_name, self.points, self.time_taken, rank)
        self.rank = rank
        #competition.leaderboard_entries.append(self)
        return rank



    def get_json(self):
        return{
            'id': self.id,
            'competition_id' : self.competition_id,
            'team_name': self.team_name,
            'points': self.points,
            'time_taken': self.time_taken
        }


    def repr(self):
        return f'<Team {self.id} : {self.team_name} - Points: {self.points}  Time Taken: {self.time_taken}>'