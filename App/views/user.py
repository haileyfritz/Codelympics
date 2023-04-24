from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from functools import wraps
from .index import index_views
from App.controllers import *
from App.models import Organization

login_manager = LoginManager()

def coordinator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Coordinator):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

@login_manager.user_loader
def load_user(user_id):
  user =  RegularUser.query.get(user_id)
  if user:
    return user
  return Admin.query.get(user_id)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

#shows home page with all organizations
@user_views.route('/home', methods = ['GET'])
@login_required
def homepage_view():
    organizations = Organization.query.all()
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None

    return render_template("organizations.html", organizations = organizations, user_type = user_type)


@user_views.route('/<string:organization_name>/competitions', methods = ['GET'])
@login_required
def organization_competitions_view(organization_name):
    organization = Organization.query.filter_by(name = organization_name).first()
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None

    return render_template("competitions.html", organization = organization, competitions = organization.competitions, user = user, user_type = user_type)


@user_views.route('/<string:competition_name>/results', methods = ['GET'])
@login_required
def competition_view(competition_name):
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None
    
    competition = Competition.query.filter_by(name = competition_name).first()
    organization = Organization.query.get(competition.organization_id)
    organization_name = organization.name
    
    teams = competition.teams

    for t in teams:
        rank = t.calculate_rank(teams, competition, t.points, t.time_taken)
    
    competition_list = []
    count = len(competition.teams)
    while count != 0:
        for t in competition.teams:
            if t.rank == count:
                competition_list.append(t) 
                count = count - 1
                break

    competition_list.reverse()

    return render_template("competitionResults.html", competition = competition, competition_list = competition_list, organization_name = organization_name, user_type = user_type)

@user_views.route('/<string:team_name>-results', methods = ['GET'])
@login_required
def team_view(team_name):
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None

    team = Team.query.filter_by(team_name = team_name).first()

    return render_template("competitionResultsTeamInfo.html", team = team, user_type = user_type)


@user_views.route('/account', methods = ['GET'])
@login_required
def account_view():
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None

    return render_template('account.html', user_type = user_type)
