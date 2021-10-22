from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def newCastleOk(lat, lng, userid):
    print("onkoOk")
    print(lat)
    print(lng)
    print(userid)
    sql = "SELECT COUNT(*) FROM CASTLES WHERE userid = :userid"
    result = db.session.execute(sql, {"userid":userid})
    count = result.fetchone()[0]
    if (count > 0):
        return "You have already built a castle! Focus on strengthening it!"
    return "True"

def user_exists(username):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone() != None