from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import jinja2

api=None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3" 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class user(db.Model):
    __tablename__='user'
    user_id=db.Column(db.String,primary_key=True,autoincrement=True)
    username=db.Column(db.String, unique=True)
    email=db.Column(db.String, unique=True)
    passward=db.Column(db.String)
class influencer(db.Model):
    __tablename__='influcener'
    influencer_id=db.Column(db.string,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    Category=db.Column(db.String)
    Niche=db.Column(db.String)
    reach=db.Column(db.Integer)
class Sponsers(db.Model):
    __tablename__='sponsers'
    Sponsers_id=db.Column(db.String,primary_key=True,autoincrement=True)
    Company_name=db.Column(db.string)
    industry=db.Column(db.string)
    budget=db.Column(db.Integer)
class campaigns(db.Model):
    campaigns_id=db.Column(db.String,primary_key=True,autoincrement=True)
    sponser=db.relationship(Sponsers,backref=   )    
class Ad_request(db.model):
    __tablename__="ad_req"
    cam    

@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)