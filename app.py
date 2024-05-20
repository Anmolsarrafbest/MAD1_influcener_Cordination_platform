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
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String, unique=True)
    email=db.Column(db.String, unique=True)
    password=db.Column(db.String)
class influencer(db.Model):
    __tablename__='influcener'
    influencer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String)
    Category=db.Column(db.String)
    Niche=db.Column(db.String)
    reach=db.Column(db.Integer)
class Sponsers(db.Model):
    __tablename__='sponsers'
    Sponsers_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Company_name=db.Column(db.String)
    industry=db.Column(db.String)
    budget=db.Column(db.Integer)
class campaigns(db.Model):
    __tablename__='campaign'
    campaigns_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sponser_id=db.Column(db.String,db.Foreigen_key(Sponsers.Sponsers_id))
    name=db.Column(db.string,nullable=False)
    description=db.Column(db.String)
    start_date=db.Column(db.String)
    end_date=db.Column(db.String)
    budget=db.Column(db.Integer)
    Visibility=db.Column(db.String)
    goals=db.Column(db.String)

class Ad_request(db.model):
    __tablename__="ad_req"
    campaigns_id=db.Column(db.Integer,db.Foreigen_key(campaigns.campaigns_id))
    sponsers_id=db.Column(db.Integer,db.Foregin_key(Sponsers.Sponsers_id))
    messages=db.Column(db.String)
    requirements=db.Column(db.String)
    payment_amount=db.Column(db.String)
    status=db.Column(db.String)
    
@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)