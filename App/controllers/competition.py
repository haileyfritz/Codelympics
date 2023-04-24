from App.models import *
from App.database import db


def get_competition(competition_name):
    competition = Competition.query.filter_by(name= competition_name).first()
    return competition


def get_all_competitions():
    return Competition.query.all()


def get_all_competitions_json():
    competitions = Competition.query.all()
    if not competitions:
        return []
    competitions = [competition.get_json() for competition in competitions]
    return competitions