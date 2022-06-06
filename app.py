from sqlite3 import Cursor
from flask import Flask, render_template, json
from flask import flash, request, redirect
from flask_mysqldb import MySQL
from forms import OrcSearchForm
from db_credentials import host, user, passwd, db
from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
app.config['SECRET_KEY'] = 'super secret string'
mysql = MySQL(app)
db_connection = connect_to_database()

# Routes 
@app.route('/')
def index():
    return render_template("index.html", title="Home")

@app.route('/index.html')
def view_home():
    return render_template("index.html", title="Home")

@app.route('/items', methods=["POST", "GET"])
def view_items():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT item_type_id, item_type FROM Item_types;"
        cursor.execute(query)
        item_type_info = cursor.fetchall()
        query = "SELECT Items.item_id, Items.item_name, Items.item_color, \
            Items.item_year, Items.item_size, Item_types.item_type FROM Items \
            LEFT JOIN Item_types ON Items.item_type_id = Item_types.item_type_id;"
        cursor.execute(query)
        item_info = cursor.fetchall()
        print(item_info)
        return render_template("items.j2", title="Items", items=item_info, item_types=item_type_info)

    elif request.method == "POST":
        # Add Item to Items table
        name = request.form['item_name']
        color = request.form['item_color']
        year = request.form['item_year']
        size = request.form['item_size']
        item_type = request.form['item_type_id']
        insert_query = query = 'INSERT INTO Items (item_name, item_color, item_year, \
            item_size, item_type_id) VALUES (%s, %s, %s, %s, %s)'
        data = (name, color, year, size, item_type)
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        #Update HTML
        query = "SELECT item_type_id, item_type FROM Item_types;"
        cursor.execute(query)
        item_type_info = cursor.fetchall()
        query = "SELECT Items.item_id, Items.item_name, Items.item_color, \
            Items.item_year, Items.item_size, Item_types.item_type FROM Items \
            LEFT JOIN Item_types ON Items.item_type_id = Item_types.item_type_id;"
        cursor.execute(query)
        item_info = cursor.fetchall()
        return render_template("items.j2", title="Items", items=item_info, item_types=item_type_info)

@app.route('/items_types', methods=["POST", "GET"])
def view_item_types():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT item_type_id, item_type FROM Item_types;"
        cursor.execute(query)
        item_type_info = cursor.fetchall()
        print(item_type_info)
        return render_template("itemTypes.j2", title="Item Types", item_types=item_type_info)

    elif request.method == "POST":
        # Add Item type to Items type table
        itype = request.form["item_type"]
        insert_query = query = 'INSERT INTO Item_types (item_type) VALUES (%s)'
        data = (itype, )
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        #Update HTML
        query = "SELECT item_type_id, item_type FROM Item_types;"
        cursor.execute(query)
        item_type_info = cursor.fetchall()
        return render_template("itemTypes.j2", title="Item Types", item_types=item_type_info)

@app.route('/jobs', methods=["POST", "GET"])
def view_jobs():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT job_id, title, num_rations, combat_role FROM Jobs;"
        cursor.execute(query)
        job_info = cursor.fetchall()
        print(job_info)
        return render_template("jobs.j2", title="Jobs", jobs=job_info)

    elif request.method == "POST":
        # Add Job to jobs table
        title = request.form['title']
        nr = request.form['num_rations']
        cr = request.form['combat_role']
        insert_query = query = 'INSERT INTO Jobs (title, num_rations, combat_role) VALUES (%s, %s, %s)'
        data = (title, nr, cr)
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        #Update HTML
        query = "SELECT job_id, title, num_rations, combat_role FROM Jobs;"
        cursor.execute(query)
        job_info = cursor.fetchall()
        return render_template("jobs.j2", title="Jobs", jobs=job_info)
    return render_template("jobs.j2", title="Jobs", jobs=job_info)

@app.route('/orc_has_items', methods=["GET", "POST"])
def view_orc_items():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT orc_id, first_name, last_name FROM Orcs;"
        cursor.execute(query)
        orcs_info = cursor.fetchall()
        query = "SELECT item_id, item_name FROM Items;"
        cursor.execute(query)
        items_info = cursor.fetchall()
        query = "SELECT Orc_has_Items.orc_item_id, Orcs.first_name, Orcs.last_name, \
                Items.item_name, Orc_has_Items.item_quantity FROM Orc_has_Items \
                LEFT JOIN Orcs on Orc_has_Items.orc_id = Orcs.orc_id \
                LEFT JOIN Items on Orc_has_Items.item_id = Items.item_id;"
        cursor.execute(query)
        orc_items_info = cursor.fetchall()
        print(orc_items_info)
        return render_template("orcHasItems.j2", title="Orc Has Items", orc_items=orc_items_info, orcs=orcs_info, items=items_info)

    if request.method == "POST":
        orc_id = request.form['orc_id']
        item_id = request.form['item_id']
        item_quantity = request.form['item_quantity']
        insert_query = query = 'INSERT INTO Orc_has_Items (orc_id, item_id, item_quantity) \
            VALUES (%s, %s, %s)'
        data = (orc_id, item_id, item_quantity)
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        # Update HTML
        query = "SELECT orc_id, first_name, last_name FROM Orcs;"
        cursor.execute(query)
        orcs_info = cursor.fetchall()
        query = "SELECT item_id, item_name FROM Items;"
        cursor.execute(query)
        items_info = cursor.fetchall()
        query = "SELECT Orc_has_Items.orc_item_id, Orcs.first_name, Orcs.last_name, \
                Items.item_name, Orc_has_Items.item_quantity FROM Orc_has_Items \
                LEFT JOIN Orcs on Orc_has_Items.orc_id = Orcs.orc_id \
                LEFT JOIN Items on Orc_has_Items.item_id = Items.item_id;"
        cursor.execute(query)
        orc_items_info = cursor.fetchall()
        print(orc_items_info)
        return render_template("orcHasItems.j2", title="Orc Has Items", orc_items=orc_items_info, orcs=orcs_info, items=items_info)


@app.route('/orc_has_skills', methods=["POST","GET"])
def view_orc_skills():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT orc_id, first_name, last_name FROM Orcs;"
        cursor.execute(query)
        orcs_info = cursor.fetchall()
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)
        skills_info = cursor.fetchall()
        query = "SELECT Orc_has_Skills.orc_skill_id, Orcs.first_name, Orcs.last_name, \
                Skills.skill_name, Orc_has_Skills.skill_level FROM Orc_has_Skills \
                LEFT JOIN Orcs on Orc_has_Skills.orc_id = Orcs.orc_id \
                LEFT JOIN Skills on Orc_has_Skills.skill_id = Skills.skill_id;"
        cursor.execute(query)
        orc_skills_info = cursor.fetchall()
        print(orc_skills_info)
        return render_template("orcHasSkills.j2", title="Orc Has Skills", orc_skills=orc_skills_info, orcs=orcs_info, skills=skills_info)

    elif request.method == "POST":
        orc_id = request.form['orc_id']
        skill_id = request.form['skill_id']
        level = request.form['skill_level']
        insert_query = query = 'INSERT INTO Orc_has_Skills (orc_id, skill_id, skill_level) \
            VALUES (%s, %s, %s)'
        data = (orc_id, skill_id, level)
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        #Update HTML
        query = "SELECT orc_id, first_name, last_name FROM Orcs;"
        cursor.execute(query)
        orcs_info = cursor.fetchall()
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)
        skills_info = cursor.fetchall()
        query = "SELECT Orc_has_Skills.orc_skill_id, Orcs.first_name, Orcs.last_name, \
                Skills.skill_name, Orc_has_Skills.skill_level FROM Orc_has_Skills \
                LEFT JOIN Orcs on Orc_has_Skills.orc_id = Orcs.orc_id \
                LEFT JOIN Skills on Orc_has_Skills.skill_id = Skills.skill_id;"
        cursor.execute(query)
        orc_skills_info = cursor.fetchall()
        print(orc_skills_info)
        return render_template("orcHasSkills.j2", title="Orc Has Skills", orc_skills=orc_skills_info, orcs=orcs_info, skills=skills_info)

@app.route('/delete_orc_skill/<int:orc_skill_id>')
def delete_orc_skill(orc_skill_id):
    query = "DELETE FROM Orc_has_Skills WHERE orc_skill_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (orc_skill_id, ))
    mysql.connection.commit()

    return redirect("/orc_has_skills")

@app.route('/edit_orc_skill/<int:orc_skill_id>', methods=["POST","GET"])
def edit_orc_skills(orc_skill_id):
    if request.method == "GET":
        query = "SELECT * FROM Orc_has_Skills where orc_skill_id = %s" % (orc_skill_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        orc_skill_info = cursor.fetchall()
        query = "SELECT orc_id, first_name, last_name FROM Orcs;"
        cursor.execute(query)
        orc_info = cursor.fetchall()
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)
        skill_info = cursor.fetchall()
        print(orc_skill_info)
        return render_template("editOrcSkills.j2", title="Edit Orc Skills", orcs=orc_info, data=orc_skill_info, skills=skill_info)

    elif request.method == "POST":
        if request.form.get("Edit_Orc_Skill"):
            osi = request.form["orc_skill_id"]
            oi = request.form["orc_id"]
            si = request.form["skill_id"]
            sl = request.form["skill_level"]
            query = "UPDATE Orc_has_Skills SET \
                orc_id = %s, \
                skill_id = %s, \
                skill_level = %s \
                WHERE Orc_has_Skills.orc_skill_id = %s;"
            data = (oi, si, sl, osi)
            cursor = mysql.connection.cursor()
            cursor.execute(query, data)
            mysql.connection.commit()

        return redirect("/orc_has_skills")

##################### Orcs ############################
# Insert
@app.route('/orcs', methods=["POST","GET"])
def view_orcs():
    search = OrcSearchForm(request.form)
    cursor = mysql.connection.cursor()
    if request.method == "GET":
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
        return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info, search=search)

    elif request.method == "POST":
        if search.name.data:
            print("Searching for name")
            print(search.name)
            orc_name = request.form[search.query.name]
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
            WHERE Orcs.first_name LIKE %s OR Orcs.last_name LIKE %s;"
            data = (orc_name, orc_name)
            cursor.execute(query, data)
            orcs_info = cursor.fetchall()
            if orcs_info == ():
                flash('No orcs found')
                return redirect("/orcs")
            print(orcs_info)
            return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info, search=search)
        elif search.reset.data:
            print("Resetting table")
            return redirect("/orcs")
        else:
            # Add Orc to Orcs table
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
        return render_template("orcs.j2", title="Orcs", orcs=orcs_info, vehicles=vehicles_info, jobs=jobs_info, search=search)

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
        query = "SELECT * FROM Orcs where orc_id = %s" % (orc_id)
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

########################## Vehicles ################################

@app.route('/vehicles', methods=["POST","GET"])
def view_vehicles():
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT vehicle_id, vehicle_type, num_spikes, color, manufacture_year FROM Vehicles;"
        cursor.execute(query)
        vehicle_info = cursor.fetchall()
        print(vehicle_info)
        return render_template("vehicles.j2", title="Vehicles", vehicles=vehicle_info)

    elif request.method == "POST":
        vt = request.form['vehicle_type']
        ns = request.form['num_spikes']
        color = request.form['color']
        my = request.form['manufacture_year']
        insert_query = query = 'INSERT INTO Vehicles (vehicle_type, num_spikes, color, manufacture_year) VALUES (%s, %s, %s, %s)'
        data = (vt, ns, color, my)
        cursor.execute(insert_query, data)
        mysql.connection.commit()

        # Update html
        cursor = mysql.connection.cursor()
        query = "SELECT vehicle_id, vehicle_type, num_spikes, color, manufacture_year FROM Vehicles;"
        cursor.execute(query)
        vehicle_info = cursor.fetchall()
        print(vehicle_info)
        return render_template("vehicles.j2", title="Vehicles", vehicles=vehicle_info)

######################### DELETE VEHICLE #################################

@app.route('/delete_vehicle/<int:vehicle_id>')
def delete_vehicle(vehicle_id):
    query = "DELETE FROM Vehicles WHERE vehicle_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (vehicle_id,))
    mysql.connection.commit()

    return redirect("/vehicles")

###################### DB TEST #######################################

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
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT skill_id, skill_name FROM Skills;"
        cursor.execute(query)
        skill_info = cursor.fetchall()
        print(skill_info)
        return render_template("skills.j2", title="Skills", skills=skill_info)

    elif request.method == "POST":
        # Add Skill to Skills table
        skill_name = request.form['skill_name']
        insert_query = query = 'INSERT INTO Skills (skill_name) VALUES (%s)'
        data = (skill_name, )
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

############## Orc Has Skills #####################



############## Orc Has Skills (Delete) #####################

@app.route("/delete_OrchasSkills/<int:skill_id>")
def delete_OrchasSkills(skill_id):
    query = "DELETE FROM Orc_has_Skills WHERE skill_id = '%s';"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (skill_id,))
    mysql.connection.commit()

    return redirect("/orchasskills")

############## Orc Has Skills (Edit) #####################

@app.route("/edit_OrchasSkills/<int:orc_Id>", methods=["POST", "GET"])
def edit_OrchasSkills(orc_id):
    if request.method == "GET":
        query = "SELECT * FROM Orc_has_Skills where orc_id = %s" % (orc_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("edit_OrchasSkills.j2", title="Edit Orc has Skills", data=data, orcskills=orc_skills_info)

    if request.method == "POST":
        if request.form.get("Edit_Orc_Has_Skill"):
            skill_id = request.form['skill_id']
            skilllevel = request.form['skill_level']
            query = "UPDATE Orc_has_Skills SET \
            skill_id = %s \
            skill_level = %s \
            WHERE Orc_has_Skills.skill_level = %s;"
            data = (skill_id, skill_level)
            cursor = mysql.connection.cursor()
            cursor.execute(query, data)
            mysql.connection.commit()
        
        return redirect("/orchasskills")

############## Items (Delete) #####################

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    query = "DELETE FROM Items WHERE item_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (item_id,))
    mysql.connection.commit()

    return redirect("/items")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 61107)) 
    app.run(debug=True) 
    app.run(port=port) 

#minor test to see if this works