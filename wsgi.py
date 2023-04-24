import click, pytest, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import time
from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
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

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)

@user_cli.command("list_users", help="Lists users in the database")
@click.argument("format", default="json")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())



@user_cli.command("search_user", help="Search for user in database")
@click.argument("username", default="bobby123")
def search_user_command(username):
    user = get_user(username)
    print(user.repr())


@user_cli.command("search_comp", help="Search for competition in database")
@click.argument("competition_name", default="Runtime_Competition")
def search_comeptition_command(competition_name):
    competition = get_competition(competition_name)
    print(competition.repr())


@user_cli.command("search_team", help="Search for team in database")
@click.argument("team_name", default="Program_Panthers")
def search_team_command(team_name):
    team = get_team(team_name)
    print(team.repr())


@user_cli.command("create_user", help="Creates new user")
@click.argument("first_name", default = "Jim")
@click.argument("last_name", default = 'Hopper')
@click.argument("email", default = 'jim@mail.com')
@click.argument("username", default = 'jim123')
@click.argument("password", default = 'jimpass')
def create_user_command(first_name, last_name, email, username, password):
    create_user(first_name, last_name, email, username, password)
    print('User created!')


@user_cli.command("create_coordinator", help="Creates new coordinator")
@click.argument("first_name", default = "Time")
@click.argument("last_name", default = 'Styles')
@click.argument("email", default = 'tim@mail.com')
@click.argument("username", default = 'tim123')
@click.argument("password", default = 'timpass')
@click.argument("organization_name", default = 'Google')
def create_coordinator_command(first_name, last_name, email, username, password, organization_name):
    create_coordinator(first, last_name, email, username, password, organization_name)
    print('Coordinator created!')

app.cli.add_command(user_cli) # add the group to the cli


'''
Coordinator Commands
'''
coordinator_cli = AppGroup('coordinator', help='Coordinator object commands') 

@coordinator_cli.command("add_comp", help="Add competition")
@click.argument("competition_name", default = "Runtime_Competition")
@click.argument("start_time", default = '12:00')
@click.argument("end_time", default = '12:00')
@click.argument("coordinator_username", default = 'jane123')
def add_competition_command(coordinator_username, competition_name, start_time, end_time):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    competition = user.add_competition(competition_name, start_time, end_time)
    if not competition:
        print('Competition could not be added.')
        return
    print('Competition added.')

# Create a time object with hours, minutes, and seconds
#my_time = time(12, 34, 56)  # Represents 12:34:56


@coordinator_cli.command("edit_comp", help="Edit competition")
@click.argument("competition_name", default = "Hackathon")
@click.argument("start_time", default = '10:00')
@click.argument("end_time", default = '12:00')
@click.argument("coordinator_username", default = 'jane123')
@click.argument("competition_id", default = 1)
def edit_competition_command(coordinator_username, competition_id, competition_name, start_time, end_time):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    competition = user.edit_competition(competition_id, competition_name, start_time, end_time)
    if not competition:
        print('Competition could not be edited.')
        return
    print('Competition edited.')


@coordinator_cli.command("remove_comp", help="Remove competition")
@click.argument("coordinator_username", default = 'jane123')
@click.argument("competition_id", default = 1)
def edit_competition_command(coordinator_username, competition_id):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    competition = user.remove_competition(competition_id)
    if not competition:
        print('Competition could not be removed.')
        return
    print('Competition removed.')


@coordinator_cli.command("list_competitions", help="Lists all competitions in the database")
@click.argument("format", default="json")
def list_competition_command(format):
    if format == 'string':
        print(get_all_competitions())
    else:
        print(get_all_competitions_json())


@coordinator_cli.command("add_team", help="Add Team to a competition")
@click.argument("team_name", default = "Program_Panthers")
@click.argument("points", default = '100')
@click.argument("coordinator_username", default = 'jane123')
@click.argument("competition_name", default = 'Runtime_Competition')
@click.argument("time_taken", default = '1:20')
def add_team_command(coordinator_username, competition_name, team_name, points, time_taken):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    competition = get_competition(competition_name)
    if competition:
        competition_id = competition.id

    if not competition:
        print('Competition not found!')
        return None

    team = user.add_team(competition.id, team_name, points, time_taken)
    if not team:
        print('Team could not be added.')
        return
    print('Team added.')


@coordinator_cli.command("edit_team", help="Edit team")
@click.argument("competition_name", default = "Runtime_Competition")
@click.argument("team_name", default = 'AI_Squad')
@click.argument("points", default = '120')
@click.argument("time_taken", default = '1:30')
@click.argument("team_id", default = 1)
@click.argument("coordinator_username", default = 'jane123')
def edit_team_command(coordinator_username, competition_name, team_id, team_name, points, time_taken):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    competition = get_competition(competition_name)
    team = user.edit_team(competition.id, team_id, team_name, points, time_taken)
    if not team:
        print('Team could not be edited.')
        return
    print('Team edited.')


@coordinator_cli.command("remove_team", help="Remove team")
@click.argument("coordinator_username", default = 'jane123')
@click.argument("team_id", default = 1)
def remove_team_command(coordinator_username, team_id):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    team = user.remove_team(team_id)
    if not team:
        print('Team could not be removed.')
        return
    print('Competition removed.')


@coordinator_cli.command("list_teams", help="Lists all teams in the database")
@click.argument("format", default="json")
def list_team_command(format):
    if format == 'string':
        print(get_all_teams())
    else:
        print(get_all_teams_json())


@coordinator_cli.command("list_comp_teams", help="Lists all teams for a particular competition")
@click.argument("format", default="json")
@click.argument("competition_name", default="Hackathon")
def list_team_command(format, competition_name):
    if format == 'string':
        print(get_all_competition_teams(competition_name))
    else:
        print(get_all_competition_teams_json(competition_name))

app.cli.add_command(coordinator_cli) # add the group to the cli


@coordinator_cli.command("add_member", help="Add team member to team")
@click.argument("coordinator_username", default = 'jane123')
@click.argument("team_name", default = 'Program_Panthers')
@click.argument("username", default = 'bobby123')
def add_member_command(coordinator_username, team_name, username):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    team = get_team(team_name)
    if not team:
        print('Team not found!')
        return None

    member = user.add_team_member(team.id, username)
    if not member:
        print('Team member could not be added.')
        return
    print('Team member added.')


@coordinator_cli.command("remove_member", help="Remove team member to team")
@click.argument("coordinator_username", default = 'jane123')
@click.argument("team_name", default = 'Program_Panthers')
@click.argument("username", default = 'bobby123')
def remove_member_command(coordinator_username, team_name, username):
    user = get_coordinator(coordinator_username)
    if not user:
        print('Coordinator not found!')
        return None

    team = get_team(team_name)
    if not team:
        print('Team not found!')
        return None

    member = user.remove_team_member(team.id, username)
    if not member:
        print('Team member could not be removed.')
        return
    print('Team member removed.')


@coordinator_cli.command("list_team_members", help="Lists all team members of a team in the database")
@click.argument("format", default="json")
@click.argument("team_id", default=1)
def list_team_command(format, team_id):
    if format == 'string':
        print(get_all_team_members(team_id))
    else:
        print(get_all_team_members_json(team_id))

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)