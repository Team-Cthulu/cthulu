from flask import Flask, render_template, json
from flask import request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
mysql = MySQL(app)
db_connection = connect_to_database()

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

##################### Orcs ############################
# Insert

@app.route('/orcs', methods=["POST","GET"])
def view_orcs():
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        query = "SELECT job_id, title FROM Jobs;"
        cursor.execute(query)
        jobs_info = cursor.fetchall()
        query = "SELECT vehicle_id, vehicle_type FROM Vehicles;"
        cursor.execute(query)
        vehicles_info = cursor.fetchall()
        query = "SELECT Orcs.orc_id, Orcs.first_name, Orcs.last_name, Orcs.height_inches, Orcs.weight_lb, \
        Orcs.birth_date, Orcs.combat_ready, Orcs.conscription_date, \
        Orcs.salary_gold_coins, Vehicles.vehicle_type, Jobs.title FROM Orcs \
        LEFT JOIN Jobs ON Orcs.job_id = Jobs.job_id \
        LEFT JOIN Vehicles ON Orcs.vehicle_id = Vehicles.vehicle_id;"
        cursor.execute(query)
        orcs_info = cursor.fetchall()
        print(orcs_info)
        return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info)

    elif request.method == "POST":
        if request.form.get("Search"):
            print("SEARCHING")
            # name = request.form["orc_search"]
            # cursor = mysql.connection.cursor()
            # query = "SELECT job_id, title FROM Jobs;"
            # cursor.execute(query)
            # jobs_info = cursor.fetchall()
            # query = "SELECT vehicle_id, vehicle_type FROM Vehicles;"
            # cursor.execute(query)
            # vehicles_info = cursor.fetchall()
            # query = "SELECT * FROM Orcs \
            # WHERE first_name LIKE %s OR last_name LIKE %s;"
            # # query = "SELECT Orcs.orc_id, Orcs.first_name, Orcs.last_name, Orcs.height_inches, Orcs.weight_lb, \
            # # Orcs.birth_date, Orcs.combat_ready, Orcs.conscription_date, \
            # # Orcs.salary_gold_coins, Vehicles.vehicle_type, Jobs.title FROM Orcs \
            # # LEFT JOIN Jobs ON Orcs.job_id = Jobs.job_id \
            # # LEFT JOIN Vehicles ON Orcs.vehicle_id = Vehicles.vehicle_id \
            # # WHERE first_name LIKE %s OR last_name LIKE %s;"
            # data = (name, name)
            # cursor.execute(query, data)
            # orcs_info = cursor.fetchall()
            # print(orcs_info)
            # return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info)
        
        # elif request.method == "POST":
        else:
            # Add Orc to Orcs table
            cursor = mysql.connection.cursor()
            fname = request.form['first_name']
            lname = request.form['last_name']
            height = request.form['height_inches']
            weight = request.form['weight_lb']
            bdate = request.form['birth_date']
            combat = request.form['combat_ready']
            conscription = request.form['conscription_date']
            salary = request.form['salary_gold_coins']
            vehicle = request.form['vehicle_id']
            job = request.form['job_id']
            if job == "" and vehicle == "":
                insert_query = query = 'INSERT INTO Orcs (first_name, last_name, height_inches, weight_lb, birth_date, combat_ready, conscription_date, salary_gold_coins) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                data = (fname, lname, height, weight, bdate, combat, conscription, salary)
                cursor.execute(insert_query, data)
            if job == "":
                insert_query = query = 'INSERT INTO Orcs (first_name, last_name, height_inches, weight_lb, birth_date, combat_ready, conscription_date, salary_gold_coins, vehicle_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                data = (fname, lname, height, weight, bdate, combat, conscription, salary, vehicle)
                cursor.execute(insert_query, data)
                
            if vehicle == "":
                insert_query = query = 'INSERT INTO Orcs (first_name, last_name, height_inches, weight_lb, birth_date, combat_ready, conscription_date, salary_gold_coins, job_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                data = (fname, lname, height, weight, bdate, combat, conscription, salary, job)
                cursor.execute(insert_query, data)

            else:
                insert_query = query = 'INSERT INTO Orcs (first_name, last_name, height_inches, weight_lb, birth_date, combat_ready, conscription_date, salary_gold_coins, vehicle_id, job_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                data = (fname, lname, height, weight, bdate, combat, conscription, salary, vehicle, job)
                cursor.execute(insert_query, data)
            mysql.connection.commit()

            # Update html
            cursor = mysql.connection.cursor()
            query = "SELECT job_id, title FROM Jobs;"
            cursor.execute(query)
            jobs_info = cursor.fetchall()
            query = "SELECT vehicle_id, vehicle_type FROM Vehicles;"
            cursor.execute(query)
            vehicles_info = cursor.fetchall()
            query = "SELECT * FROM Orcs;"
            cursor.execute(query)
            orcs_info = cursor.fetchall()
            print(orcs_info)
            return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info)

########### DELETE ORC #################
@app.route('/delete_orc/<int:orc_id>')
def delete_orc(orc_id):
    query = "DELETE FROM Orcs WHERE orc_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (orc_id,))
    mysql.connection.commit()

    return redirect("/orcs")

########### EDIT ORC #################

@app.route("/edit_orc/<int:orc_id>", methods=["POST", "GET"])
def edit_orc(orc_id):
    if request.method == "GET":
        query = "SELECT * FROm Orcs where orc_id = %s" % (orc_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        query = "SELECT job_id, title FROM Jobs;"
        cursor.execute(query)
        jobs_info = cursor.fetchall()
        query = "SELECT vehicle_id, vehicle_type FROM Vehicles;"
        cursor.execute(query)
        vehicles_info = cursor.fetchall()
        return render_template("edit_orc.j2", title="Edit Orc", data=data, jobs=jobs_info, vehicles=vehicles_info)

    if request.method == "POST":
        if request.form.get("Edit_Orc"):
            orc_id = request.form['orc_id']
            fname = request.form['first_name']
            lname = request.form['last_name']
            height = request.form['height_inches']
            weight = request.form['weight_lb']
            bdate = request.form['birth_date']
            combat = request.form['combat_ready']
            conscription = request.form['conscription_date']
            salary = request.form['salary_gold_coins']
            vehicle = request.form['vehicle_id']
            job = request.form['job_id']
            query = "UPDATE Orcs SET \
            first_name = %s, \
            last_name = %s, \
            height_inches = %s, \
            weight_lb = %s, \
            birth_date = %s, \
            combat_ready = %s, \
            conscription_date = %s, \
            salary_gold_coins = %s, \
            vehicle_id = %s, \
            job_id = %s \
            WHERE Orcs.orc_id = %s;"
            data = (fname, lname, height, weight, bdate, \
            combat, conscription, salary, vehicle, job, orc_id)
            cursor = mysql.connection.cursor()
            cursor.execute(query, data)
            mysql.connection.commit()
        
        return redirect("/orcs")

@app.route('/search', methods= ["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form["orc_name"]
        cursor = mysql.connection.cursor()
        query = "SELECT job_id, title FROM Jobs;"
        cursor.execute(query)
        jobs_info = cursor.fetchall()
        query = "SELECT vehicle_id, vehicle_type FROM Vehicles;"
        cursor.execute(query)
        vehicles_info = cursor.fetchall()
        query = "SELECT Orcs.orc_id, Orcs.first_name, Orcs.last_name, Orcs.height_inches, Orcs.weight_lb, \
        Orcs.birth_date, Orcs.combat_ready, Orcs.conscription_date, \
        Orcs.salary_gold_coins, Vehicles.vehicle_type, Jobs.title FROM Orcs \
        LEFT JOIN Jobs ON Orcs.job_id = Jobs.job_id \
        LEFT JOIN Vehicles ON Orcs.vehicle_id = Vehicles.vehicle_id \
        WHERE first_name LIKE %s OR last_name LIKE %s;"
        data = (name, name)
        cursor.execute(query, data)
        orcs_info = cursor.fetchall()
        print(orcs_info)
        return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info)
    return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info)


@app.route('/vehicles')
def view_vehicles():
    return render_template("vehicles.j2", title="Vehicles", vehicles=vehicle_info)

@app.route('/db-test')
def test_db_connection():
    print("Testing database using credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from Orcs;"
    cursor = execute_query(db_connection, query)
    result = json.dumps(cursor.fetchall())
    return result

############## Skills #####################

@app.route('/skills', methods=["POST","GET"])
def view_skills():
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)

        skill_info = cursor.fetchall()
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)
        skill_info = cursor.fetchall()
        print(skill_info)
        return render_template("skills.j2", title="Skills", skills=skill_info)

    elif request.method == "POST":
        if request.form.get("Search"):
            print("SEARCHING")

        else:
            cursor = mysql.connection.cursor()
            skill_id = request.form['skill_id']
            skill_name = request.form['skill_name']
            if skill_name == "":
                insert_query = query = 'INSERT INTO Skills (skill_id) VALUES (%s)'
                data = (skill_id)
                cursor.execute(insert_query, data)
            if skill_id == "":
                insert_query = query = 'INSERT INTO Skills (skill_name) VALUES (%s)'
                data = (skill_id)
                cursor.execute(insert_query, data)
            else:
                insert_query = query = 'INSERT INTO Skills (skill_id, skill_name) VALUES (%s, %s)'
                data = (skill_id, skill_name)
                cursor.execute(insert_query, data)
            mysql.connection.commit()

            # Update html
            cursor = mysql.connection.cursor()
            query = "SELECT skill_id, skill_name FROM Skills;"
            cursor.execute(query)
            skill_info = cursor.fetchall()
            print(skill_info)
            return render_template("skills.j2", title="Skills", skills=skill_info)

############## Skills (Delete) #####################

@app.route('/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    query = "DELETE FROM Skills WHERE skill_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (skill_id,))
    mysql.connection.commit()

    return redirect("/skills")

############## Skills (Edit) #####################

@app.route("/edit_skill/<int:skill_id>", methods=["POST", "GET"])
def edit_skill(skill_id):
    if request.method == "GET":
        query = "SELECT * FROM Skills where skill_id = %s" % (skill_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("edit_skill.j2", title="Edit Skill", data=data, skills=skill_info)

    if request.method == "POST":
        if request.form.get("Edit_Skill"):
            skill_id = request.form['skill_id']
            skillname = request.form['skill_name']
            query = "UPDATE Skills SET \
            skill_name = %s \
            WHERE Skills.skill_id = %s;"
            data = (skillname, skill_id)
            cursor = mysql.connection.cursor()
            cursor.execute(query, data)
            mysql.connection.commit()
        
        return redirect("/skills")

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
    port = int(os.environ.get('PORT', 61422)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 

#minor test to see if this works