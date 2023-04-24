from flask import Flask, Blueprint, render_template,url_for, redirect, request, flash, make_response, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from functools import wraps
from App.controllers import *

def coordinator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Coordinator):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

coordinator_views = Blueprint('coordinator_views', __name__, template_folder='../templates')

@coordinator_views.route('/coordinator', methods = ['GET'])
@coordinator_required
def coordinator_view():
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    organization = Organization.query.get(user.organization_id)

    return render_template('ResultsManager.html', organization = organization.name)


@coordinator_views.route('/coordinator/add-competition', methods = ['GET'])
def add_competition_view():
    return render_template('addCompetition.html')


@coordinator_views.route('/coordinator/add-competition', methods = ['POST'])
@coordinator_required
def add_competition_action():
    data = request.form

    coordinator = Coordinator.query.get(current_user.id)
    newcompetition = coordinator.add_competition(data['name'], data['start_time'], data['end_time'])
    if not newcompetition:
        flash('Competition name taken!') 
        return redirect('/coordinator/add-competition')
    else:
        flash("Competition added!")
        return render_template('addEditResults.html', competition = data['name'])


@coordinator_views.route('/coordinator/edit-results/<string:competition_name>', methods = ['POST'])
@coordinator_required
def add_team_action(competition_name):
    data = request.form

    coordinator = Coordinator.query.get(current_user.id)
    competition = Competition.query.filter_by(name = competition_name).first()

    newteam = coordinator.add_team(competition.id, data['team-name'], data['team-points'], data['team-time'])
    if not newteam:
        flash('Team name taken!') 
    else:
        members = data['team-members'].split(',')
        for m in members:
            username = m.strip()
            user = User.query.filter_by(username = username).first()
            if user:
                newmember = coordinator.add_team_member(newteam.id, user.username)
                if not newmember:
                    flash("Could not add member!")
            else:
                flash ("Could not find member!")


        flash("Team added!")

    return render_template('addEditResults.html', competition = competition.name, teams = competition.teams)


@coordinator_views.route('/<string:competition_name>/dashboard', methods = ['GET'])
@coordinator_required
def dashboard_view(competition_name):
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None
    
    return render_template('dashboard.html', competition = competition_name, user_type = user_type)


@coordinator_views.route('/<string:competition_name>/manage-results', methods = ['GET'])
@coordinator_required
def manage_results_view(competition_name):
    user = Coordinator.query.filter_by(first_name = current_user.first_name).first()
    if isinstance(user, Coordinator):
        user_type = 'Coordinator'
    else:
        user_type = None
    
    return render_template('addEditResults.html', competition = competition_name,  teams = competition.teams)


@coordinator_views.route("/<string:competition_name>/remove-team/<int:team_id>", methods = ['GET'])
@coordinator_required
def remove_team_action(competition_name, team_id):
    competition = Competition.query.filter_by(name = competition_name).first()
    coordinator = Coordinator.query.get(current_user.id)

    team = coordinator.remove_team(team_id)
    if not team:
        flash('Team could not be found')
    else:
        flash('Team removed!')

    return render_template('addEditResults.html', competition = competition_name,  teams = competition.teams)