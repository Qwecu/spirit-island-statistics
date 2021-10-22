from app import app
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv


from db import db
import users
import castles
import random
import math


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spiritstatistics")
def spiritstatistics():
    data = db.session.execute("""WITH allSpiritsAndAdversaries AS (
select spirit.id spiritid, spirit.name spiritname, a.id adversaryId, a.name adversaryName
FROM spirit
FULL OUTER JOIN adversary a ON 1 = 1
), maxVictories AS (
SELECT MAX(al.level) maxVictory,
AVG(CAST(al.level AS float)) avgLevelDefeated,
COUNT(DISTINCT g.id) totalVictories,
al.adversaryId adversaryId, gps.spiritId
FROM
adversaryLevel al
INNER JOIN game_adversaryLevel gal ON gal.adversaryLevelId = al.id
LEFT JOIN game_player_spirit gps ON gps.gameId = gal.gameId
LEFT JOIN game g ON g.id = gps.gameId
WHERE win = '1'
--AND playerId = 12
GROUP BY  gps.spiritId, al.adversaryId)
SELECT * FROM allSpiritsAndAdversaries asaa
LEFT JOIN maxVictories mv ON mv.adversaryId = asaa.adversaryId AND mv.spiritId = asaa.spiritid
ORDER BY COALESCE(maxVictory, 0) desc, COALESCE(totalVictories, 0) desc,  adversaryName desc, spiritname desc""")
    return render_template("spiritstatistics.html", datarows = data)

@app.route("/listingredients")
def listingredients():
    result = db.session.execute("SELECT COUNT(*) FROM ingredients")
    count = result.fetchone()[0]
    result = db.session.execute("\
        select CONCAT(ingredient, ' ', price::text, ' € (', priceperunit::NUMERIC(6, 2)::text, ' €/', measureunit.name, ')') \
        from ingredients \
        left join measureunit on measureunit.id = ingredients.measureunit_id \
        order by ingredient")
    ingredients = result.fetchall()
    return render_template("listingredients.html", count=count, ingredients=ingredients)

@app.route("/newingredient")
def newingredient():
    result = db.session.execute("select id, name from measureunit")
    units = result.fetchall()
    result = db.session.execute("select id, name from filter")
    filters = result.fetchall()
    return render_template("newingredient.html", units = units, filters = filters)

@app.route("/sendingredient", methods=["POST"])
def sendingredient():
    if users.loggedin() == False:
        return render_template("index.html", error="Tämä ominaisuus on vain kirjautuneille käyttäjille")
    if users.csrf() != request.form["csrf_token"]:
        abort(403)

    ingredient = request.form["ingredient"]
    price = request.form["price"]
    amount = request.form["amount"]
    unit = request.form["unitradio"]
    #sql

    try:
        sql = "INSERT INTO ingredients (ingredient, price, amount, measureunit_id) VALUES (:ingredient, :price, :amount, :unit) RETURNING id"
        result = db.session.execute(sql, {"ingredient":ingredient, "price":price, "amount":amount, "unit":unit })
        ingredientid = result.fetchone()[0]

        sql = "SELECT id FROM filter"
        result = db.session.execute(sql)

        filters = request.form.getlist("filtercheck")

        if(len(filters)) > 0:
            sql = "INSERT INTO filter_ingredient (filter_id, ingredient_id)  VALUES "
            for id in filters:
                sql += "("
                sql += str(int(id))
                sql += ", :ingredientid)"
            sql = sql.replace(")(", "), (")
            db.session.execute(sql,{"ingredientid":ingredientid})


        db.session.commit()
        return redirect("/listingredients")
    except:
        return render_template("index.html", error= "Tapahtui virhe. Huomaathan, että ainesosaa ei saa olla ennestään tietokannassa ja sen hinnan on oltava yli 0.")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    error_message = users.login(username, password)
    if error_message == "":
        return redirect("/")
    elif error_message == "No such user":
        users.register(username, password)
        return render_template("index.html", message="Sinut on nyt rekisteröity käyttäjäksi")
    else:
        return render_template("index.html", error=error_message)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/generaterecipe")
def generaterecipe():
    result = db.session.execute("select id, name from filter")
    filters = result.fetchall()
    return render_template("generaterecipe.html", filters = filters)

@app.route("/generaterecipepost", methods=["POST"])
def generaterecipepost():
    if users.loggedin() == False:
        return render_template("index.html", error="Tämä ominaisuus on vain kirjautuneille käyttäjille")
    if users.csrf() != request.form["csrf_token"]:
        abort(403)
    try:
        budget = float(request.form["budget"])
    except:
        return render_template("index.html", error="Anna budjetti numeroina, desimaalierottimena piste")    
    if (budget <= 0):
        return render_template("index.html", error="Noin halvalla et ikävä kyllä voi päästä")

    max_ingredient_amount = int(math.sqrt(random.random() * 80) + 1)
    #result = db.session.execute("SELECT COUNT(*) FROM ingredients")
    #count = result.fetchone()[0]
    strjoin = ""
    strwhere = ""

    filters = request.form.getlist("filtercheck")

    if(len(filters)) > 0:
        strwhere = "WHERE 1 = 1 "
        for id in filters:
            filterid = str(int(id))
            alias = "al" + filterid
            strjoin += "	INNER JOIN filter_ingredient " + alias + " ON " + alias + ".ingredient_id = ingredients.id "
            strwhere += "AND " + alias + ".filter_id = " + filterid + " "

    strj = "	INNER JOIN filter_ingredient a1 ON a1.ingredient_id = ingredients.id "

    stringsql = \
        "SELECT *, ROW_NUMBER() OVER (ORDER by id) as htmlid " + \
        "FROM  ( " + \
        " SELECT DISTINCT 1 + trunc(random() *  " + \
        "   (select COUNT(*) from ingredients " + \
        strjoin + \
        strwhere + \
        "	) " + \
        " )::integer AS id " + \
        " FROM   generate_series(1, :max_ingredient_amount) g " + \
        " ) r " + \
        " JOIN    " + \
        "( " + \
        "select ROW_NUMBER () OVER (ORDER BY id) as id, ingredient, id as originalid, price from ingredients " + \
        strjoin + \
        strwhere + \
        ") validfoods " + \
        "USING (id) " \
        "ORDER BY id; "
    
    recipe = db.session.execute(stringsql,{"max_ingredient_amount": max_ingredient_amount})

    
    weights = []
    weightsum = 0

    rowcount = recipe.rowcount

    for r in range(rowcount):
        weight = random.randint(1,10)
        weights.append(weight)
        weightsum += weight

    modifier = 1 / (weightsum * 1.0 / budget)

    totalprice = 0
    cheapestindex = 0
    cheapestprice = 0
    weighedrecipe = []

    currentindex = 0
    for food in recipe:
        if food[3] < cheapestprice or cheapestprice == 0:
            cheapestprice = food[3]
            cheapestindex = currentindex

        individualbudget = modifier * weights[currentindex]
        count = int(individualbudget / float(food[3]))
        totalprice += count * food[3]
        weighedrecipe.append([food[0], food[1], food[2], food[3], count, food[4]])
        #test += (str(food[0]) + " " + str(food[1]) + " " + str(food[2]) + " " + str(food[3]) + " " + str(count) + "\n")


        currentindex = currentindex + 1
        
    #moneyleft = budget - totalprice
    #if cheapestprice > 0:
        #morestuffamount = weighedrecipe[cheapestindex]
        #TODO add more stuff to the list to better utilize budget
    if len(weighedrecipe) == 0:
        return redirect("index.html", error="Ostoslistaa ei voitu muodostaa. Yritä höllentää kriteerejäsi")
    return render_template("showrecipe.html", items = weighedrecipe, totalprice = totalprice, count = rowcount)
    #return str(ingredient_amount)

@app.route("/showrecipe/<int:id>")
def showexistingrecipe(id):
    sql = """SELECT name, SUM(count * price)
    FROM recipes r
    INNER JOIN recipes_ingredients on r.id = recipe_id
    INNER JOIN ingredients i on i.id = ingredient_id
    WHERE r.id = :id
    GROUP BY name"""

    result = db.session.execute(sql, {"id":id}).fetchone()
    name = result[0]
    price = result[1]

    sql = """SELECT 0, ingredient, 0, price, count
    FROM recipes r
    INNER JOIN recipes_ingredients on r.id = recipe_id
    INNER JOIN ingredients i on i.id = ingredient_id
    WHERE r.id = :id"""

    result = db.session.execute(sql, {"id":id})
    return render_template("showrecipe.html", items = result, recipe_name = name,  totalprice = price)

@app.route("/sendrecipe", methods=["POST"])
def sendrecipe():
    if users.loggedin() == False:
        return render_template("index.html", error="Tämä ominaisuus on vain kirjautuneille käyttäjille")

    if users.csrf() != request.form["csrf_token"]:
        abort(403)
        
    try:
        ic = request.form["count"]
        ingredientcount = int(ic)
        name = request.form["name"]

        sql = "INSERT INTO recipes (name) VALUES (:name) RETURNING id; "
        result = db.session.execute(sql, {"name":name})
        recipe_id = result.fetchone()[0]
        sql = "INSERT INTO recipes_ingredients (recipe_id, ingredient_id, count) VALUES "

        for x in range(ingredientcount):
            i = str(x + 1)
            id = str(int(request.form["hiddenId" + i]))
            count = str(int(request.form["hiddenCount" + i]))
            sql += (" (" + ":recipe_id, " + id + ", " + count + ")")
            if(x < (ingredientcount - 1)):
                sql += ","

        db.session.execute(sql, {"recipe_id":recipe_id})
        db.session.commit()
        return render_template("index.html", message = "Ostoslista tallennettu")
    except:
        return render_template("index.html", error = "Tapahtui virhe. Annathan ostoslistalle nimen, ja sellaisen, joka ei ole ennestään käytössä")


@app.route("/recipes")
def recipes():
    result = db.session.execute("SELECT COUNT(*) FROM recipes")
    count = result.fetchone()[0]
    result = db.session.execute("""
        SELECT id, name FROM recipes
    """)
    recipes = result.fetchall()
    return render_template("recipes.html", count=count, recipes=recipes)

@app.route("/map")
def map():
    sql = "SELECT id, userid, name, lat, lng, diameter FROM CASTLES "
    oldcastles = db.session.execute(sql)

    return render_template("kartta.html", oldcastles=oldcastles)

@app.route("/devblog")
def devblog():
    return render_template("devblog.html")

@app.route("/createcastle", methods=["POST"])
def createcastle():
    

    if users.loggedin() == False:
        return render_template("index.html", error="Tämä ominaisuus on vain kirjautuneille käyttäjille")


    if users.csrf() != request.form["csrf_token"]:
        abort(403)
        
    try:
        print("cc")
        lat = float(request.form["lat"])
        lng = float(request.form["lng"])
        name = request.form["castle"]

        if name == "":
            return render_template("index.html", error = "Your castle must have a name!")

        print("saa")

        approved = castles.newCastleOk(lat, lng, users.userid())

        if (approved == "True"):
            sql = "INSERT INTO castles(name, userid, lat, lng, diameter) VALUES(:name, :userid, :lat, :lng, 500)  " 
            print("test")
            print(users.userid())
            result = db.session.execute(sql, {"name":request.form["castle"], "userid":users.userid(), "lat":lat, "lng":lng })
            db.session.commit()
            return render_template("index.html", message = "New castle created! Let it be glorious!")
        else :
            return render_template("index.html", error = approved)
    except:
        return render_template("index.html", error = "Tapahtui virhe.")
