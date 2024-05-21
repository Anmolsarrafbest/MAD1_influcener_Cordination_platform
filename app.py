from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import jinja2

api=None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3" 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# defining models

class user(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String, unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)

class influencer(db.Model):
    __tablename__='influcener'
    influencer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,db.ForeignKey(user.username))
    Category=db.Column(db.String)
    Niche=db.Column(db.String)
    reach=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey(user.user_id))

class Sponsers(db.Model):
    __tablename__='sponsers'
    Sponsers_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Company_name=db.Column(db.String)
    industry=db.Column(db.String)
    budget=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey(user.user_id))

class campaigns(db.Model):
    __tablename__='campaign'
    campaigns_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sponser_id=db.Column(db.String,db.ForeignKey(Sponsers.Sponsers_id))
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String)
    start_date=db.Column(db.String)
    end_date=db.Column(db.String)
    budget=db.Column(db.Integer)
    Visibility=db.Column(db.String)
    goals=db.Column(db.String)

class Ad_request(db.Model):
    __tablename__="ad_req"
    adreq_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    campaigns_id=db.Column(db.Integer,db.ForeignKey(campaigns.campaigns_id))
    sponsers_id=db.Column(db.Integer,db.ForeignKey(Sponsers.Sponsers_id))
    messages=db.Column(db.String)
    requirements=db.Column(db.String)
    payment_amount=db.Column(db.String)
    status=db.Column(db.String)

@app.route("/",methods=["GET"])
def home():
    return render_template("logging.html")

@app.route("/",methods=['POST'])
def returns():
    username=request.form['username']
    password=request.form['pass']
    role=request.form['role']
    if role =="Admin":
        if username=="admin_anmol" and password=="india@2024":
            return render_template('admin.html')
        else:
            return render_template('Notadmin.html')
    elif role=="Sponsers":
        return render_template("sponser.html")
    else:
        return render_template('user.html')

if __name__=="__main__":
    app.run(debug=True)