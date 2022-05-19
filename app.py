from flask import Flask, render_template
from flask import request, redirect
# from flask import MySQL
from db_credentials import host, user, passwd, db
# from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

# app.config['MYSQL_HOST'] = host
# app.config['MYSQL_USER'] = user
# app.config['MYSQL_PASSWORD'] = passwd
# app.config['MYSQL_DB'] = db
# mysql = MySQL(app)

# Routes 
@app.route('/')
def index():
    return render_template("index.html", title="Home")

@app.route('/index.html')
def view_home():
    return render_template("index.html", title="Home")

@app.route('/items')
def view_items():
    return render_template("items.j2", title="Items", items=item_info)

@app.route('/items_types')
def view_item_types():
    return render_template("itemTypes.j2", title="Item Types", item_types=item_type_info)

@app.route('/jobs')
def view_jobs():
    return render_template("jobs.j2", title="Jobs", jobs=job_info)

@app.route('/orc_has_items')
def view_orc_items():
    return render_template("orcHasItems.j2", title="Orc Has Items", orc_items=orc_items_info)

@app.route('/orc_has_skills')
def view_orc_skills():
    return render_template("orcHasSkills.j2", title="Orc Has Skills", orc_skills=orc_skills_info)

@app.route('/orcs')
def view_orcs():
    return render_template("orcs.j2", title="Orcs", orcs=orcs_info)

@app.route('/skills')
def view_skills():
    return render_template("skills.j2", title="Skills", skills=skill_info)

@app.route('/vehicles')
def view_vehicles():
    return render_template("vehicles.j2", title="Vehicles", vehicles=vehicle_info)

# @app.route('/db-test')
# def test_db_connection():
#     print("Testing database using credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from Orcs;"
#     result = execute_query(db_connection_query)
#     return result

# Listener

people_from_app_py = [
{
    "name": "Thomas",
    "age": 33,
    "location": "New Mexico",
    "favorite_color": "Blue"
},
{
    "name": "Gregory",
    "age": 41,
    "location": "Texas",
    "favorite_color": "Red"
},
{
    "name": "Vincent",
    "age": 27,
    "location": "Ohio",
    "favorite_color": "Green"
},
{
    "name": "Alexander",
    "age": 29,
    "location": "Florida",
    "favorite_color": "Orange"
}
]

orcs_info = [
{
    "orc_id": 1,
    "first_name": "Orgrim",
    "last_name": "Doomhammer",
    "height_inches": 72,
    "weight_lb": 265,
    "birth_date": "1964-12-25",
    "combat_ready": 1,
    "conscription_date": "1982-04-20",
    "salary_gold_coins": 12323490,
    "vehicle_id": 2,
    "job_id": 3
},
{
    "orc_id": 2,
    "first_name": "Little",
    "last_name": "Peon",
    "height_inches": 42,
    "weight_lb": 56,
    "birth_date": "2017-06-17",
    "combat_ready": 0,
    "conscription_date": "null",
    "salary_gold_coins": 0,
    "vehicle_id": "null",
    "job_id": "null" 
},
{
    "orc_id": 3,
    "first_name": "Mother",
    "last_name": "Theresa",
    "height_inches": 62,
    "weight_lb": 185,
    "birth_date": "1956-11-17",
    "combat_ready": 1,
    "conscription_date": "1989-09-17",
    "salary_gold_coins": 711,
    "vehicle_id": 1,
    "job_id": 1 
}
]

vehicle_info = [
    {
        "vehicle_id": 1,
        "vehicle_type": "not a unicorn",
        "num_spikes": 1,
        "color": "beige",
        "manufacture_year": "2004"
    },
    {
        "vehicle_id": 2,
        "vehicle_type": "war machine",
        "num_spikes": 42,
        "color": "blood red",
        "manufacture_year": "1998"
    },
    {
        "vehicle_id": 3,
        "vehicle_type": "ice cream truck",
        "num_spikes": 7,
        "color": "teal",
        "manufacture_year": "1987"
    }
]

skill_info = [
    {
        "skill_id": 1,
        "skill_name": "fighting"
    },
    {
        "skill_id": 2,
        "skill_name": "fletching"
    },
    {
        "skill_id": 3,
        "skill_name": "cooking"
    },
]

item_info = [
    {
        "item_id": 1,
        "item_name": "Warhammer",
        "item_color": "Grey",
        "item_year": "2017",
        "item_size": "Large",
        "item_type_id": 1
    },
    {
        "item_id": 2,
        "item_name": "Lute",
        "item_color": "Beige",
        "item_year": "1998",
        "item_size": "Medium",
        "item_type_id": 4 
    },
    {
        "item_id": 3,
        "item_name": "Fork",
        "item_color": "Silver",
        "item_year": "2021",
        "item_size": "Extra Small",
        "item_type_id": 2 
    }
]

item_type_info = [
    {
        "item_type_id": 1,
        "item_type": "Weapon"
    },
    {
        "item_type_id": 2,
        "item_type": "Tool"
    },
    {
        "item_type_id": 3,
        "item_type": "Toy"
    },
    {
        "item_type_id": 4,
        "item_type": "Musical Instrument"
    },
]

job_info = [
    {
        "job_id": 1,
        "title": "Cook",
        "num_rations": 15,
        "combat_role": 0
    },
    {
        "job_id": 2,
        "title": "Peon",
        "num_rations": 10,
        "combat_role": 0 
    },
    {
        "job_id": 3,
        "title": "Warlord",
        "num_rations": 3524,
        "combat_role": 1 
    },
]

orc_items_info = [
    {
        "orc_item_id": 1,
        "first_name": "Orgrim",
        "last_name": "Doomhammer",
        "item": "Warhammer",
        "item_quantity": 1
    },
    {
        "orc_item_id": 2,
        "first_name": "Little",
        "last_name": "Peon",
        "item": "Lute",
        "item_quantity": 3 
    },
    {
        "orc_item_id": 3,
        "first_name": "Mother",
        "last_name": "Theresa",
        "item": "Fork",
        "item_quantity": 100 
    },
]

orc_skills_info = [
    {
        "orc_skill_id": 1,
        "first_name": "Orgrim",
        "last_name": "Doomhammer",
        "skill": "Fighting",
        "skill_level": 60 
    },
    {
        "orc_skill_id": 2,
        "first_name": "Orgrim",
        "last_name": "Doomhammer",
        "skill": "Cooking",
        "skill_level": 2 
    },
    {
        "orc_skill_id": 3,
        "first_name": "Mother",
        "last_name": "Theresa",
        "skill": "Cooking",
        "skill_level": 40 
    },
    {
        "orc_skill_id": 4,
        "first_name": "Little",
        "last_name": "Peon",
        "skill": "Fighting",
        "skill_level": 1 
    },
]
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 61420)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 