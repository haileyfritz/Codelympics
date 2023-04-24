from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Organization, Team , User, Coordinator, Competition
from App.controllers import create_user
import csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('Bob', 'Smith', 'bob@mail.com', 'bob', 'bobpass')
   
    with open('organizations.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_org = Organization(name =row['organization_name'])
            db.session.add(new_org)
    db.session.commit() 


    with open('coordinators.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            organization = Organization.query.filter_by(name = row['organization']).first()
            organization_id = organization.id
            new_coord = Coordinator(
                    organization_id = organization_id,
                    first_name =row['first_name'], 
                    last_name =row['last_name'], 
                    email =row['email'], 
                    username =row['username'], 
                    password =row['password']
                )
            db.session.add(new_coord)
    db.session.commit() 
  
    with open('competitions.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            organization = Organization.query.filter_by(name = row['organization']).first()
            organization_id = organization.id
            new_comp = Competition(
                    organization_id = organization_id,
                    name =row['competition_name'], 
                    start_time =row['start_time'], 
                    end_time =row['end_time']
                )
            organization.competitions.append(new_comp)
            db.session.add(new_comp)
    db.session.commit() 

    with open('teams.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            competition = Competition.query.filter_by(name = row['competition_name']).first()
            competition_id = competition.id
            new_team = Team(
                    competition_id = competition_id,
                    team_name =row['team_name'], 
                    points =row['points'], 
                    time_taken =row['time_taken']
                )
            competition.teams.append(new_team)
            db.session.add(new_team)
            
    db.session.commit() 

    with open('users.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_user = User(
                    first_name =row['first_name'], 
                    last_name =row['last_name'], 
                    email =row['email'], 
                    username =row['username'], 
                    password =row['password']
                )
            
            team = Team.query.filter_by(team_name = row['team_name']).first()
            if team:
                team.members.append(new_user)
            db.session.add(new_user)
    db.session.commit()
    print('database intialized')

    return jsonify(message='db initialized!')