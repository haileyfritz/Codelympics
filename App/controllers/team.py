from App.models import *
from App.database import db


def get_team(team_name):
    return Team.query.filter_by(team_name= team_name).first()
    

def get_all_teams():
    return Team.query.all()


def get_all_teams_json():
    teams = Team.query.all()
    if not teams:
        return []
    teams = [team.get_json() for team in teams]
    return teams

def get_all_competition_teams(competition_name):
    competition = Competition.query.filter_by(name = competition_name).first()
    if not competition:
        return None
    
    competition_id = competition.id
    return Team.query.filter_by(competition_id = competition_id)


def get_all_competition_teams_json(competition_name):
    competition = Competition.query.filter_by(name = competition_name).first()
    if not competition:
        return None
    
    competition_id = competition.id

    teams = Team.query.filter_by(competition_id = competition_id)
    if not teams:
        return []
    teams = [team.get_json() for team in teams]
    return teams


def get_all_team_members(team_id):
    team = Team.query.get(team_id)
    return team.members


def get_all_team_members_json(team_id):
    team = Team.query.get(team_id)
    if not team:
        return []

    members = [member.get_json() for member in team.members]
    return members