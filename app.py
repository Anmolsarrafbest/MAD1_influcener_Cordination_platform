from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import jinja2

api=None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3" 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key = '123456789Anmol'

# defining models

class user(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String, unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String)

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
    campaignss=db.relationship('campaigns',backref="sponser",lazy=True)

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
    use2=request.form['username']
    password=request.form['pass']
    role=request.form['role']
    ans=db.session.query(user).filter(user.username==use2).first()
    passs=db.session.query(user).filter(user.password==password).first()
    if role =="Admin":
        if use2=="admin_anmol" and password=="2024":
            data=db.session.query(user).all()
            return render_template('admin.html',data=data)
        else:
            return render_template('Notadmin.html')
    elif role=="Sponsers":
        
        #write code for the who had already registerd
        if ans==None or passs==None:
            return render_template("Notregistered.html")
        elif ans.username==use2 and password==passs.password:
            id=ans.user_id
            return redirect(f"/sponserhome/{id}")
            # return render_template("sponser_home.html",ans=ans)
        else:
            return render_template("Notregistered.html")
    else:
        if ans==None or passs==None:
            return render_template("Notregistered.html")
        elif ans.username==use2 and password==passs.password:
            user1=ans.username
            return render_template("user.html",user1=user1)
        else:
            return render_template("Notregistered.html")
    
@app.route("/register",methods=["GET"])
def getdet():
    return render_template("register.html")    

@app.route("/register",methods=["POST"])
def value():
    role=request.form["role"]
    user1=request.form["username"]
    password=request.form['pass']
    ans=db.session.query(user).filter(user.username==user1).first()
    if role=="Sponsers":
        if ans==user1:
            return render_template('usernotallowed.html',ans=ans,user1=user1)
        else:
            return render_template("sponserdetails.html",ans=ans,user1=user1,password=password,role=role)
    elif role=="user":
        if ans==user1:
            return render_template('usernotallowed.html',ans=ans,user1=user1)
        else:
            
            return render_template("user_details.html",user1=user1,role=role,password=password)

    
@app.route("/login",methods=['GET'])
def loginadmin():
    data=db.session.query(user).all()
    return render_template('admin.html',data=data)

@app.route("/login_users",methods=["GET"])
def loginuser():
    det=db.session.query(user).filter(user.username==user.username)
    return render_template('all.html',details=det)

@app.route("/login_camp",methods=["GET"])
def logincamp():
    return render_template('allcamp.html')

@app.route("/sponserdetails" ,methods=["POST"])
def sponser_details():
    id=request.form["user1"]
    cname=request.form["company_name"]
    paisa=request.form["budget"]
    indus=request.form["industry"]
    usernames=request.form["user1"]
    passwords=request.form["password"]
    roles=request.form['role']
    nuser=user(username=usernames,password=passwords,role=roles)
    ans=db.session.query(user).filter(user.username==usernames).first()
    db.session.add(nuser)
    db.session.commit()
    user_det=db.session.query(user).filter(user.username==id).first() 
    print(user_det.user_id)  
    newSpon=Sponsers(Company_name=cname,budget=paisa,industry=indus,user_id=user_det.user_id) 
    db.session.add(newSpon)
    db.session.commit()
    flash('You have been successfully registered! please logg in ')    
    return render_template("logging.html")

@app.route("/userdetails",methods=["POST"])
def resolve():
    user1=request.form['username']
    pass1=request.form["pass"]
    role1=request.form["role"]
    naam=request.form['vname']
    Cate=request.form['cate']
    Niche=request.form['niche']
    reach=request.form['follows']
    nuser=user(username=user1,password=pass1,role=role1)
    db.session.add(nuser)
    db.session.commit()    
    info1=influencer(name=naam,Category=Cate,Niche=Niche,reach=reach)
    db.session.add(info1)
    db.session.commit()
    return render_template('user.html',user1=user1)

@app.route("/create_camp/<int:user_id>")
def start(user_id):
    user2 = db.session.query(user).get(user_id)
    iduser=user_id

    return render_template("just.html",user2=user2)

@app.route("/campdetails",methods=["POST"])
def campdet():
    id=request.form["userid"]
    sponser_id=db.session.query(Sponsers).filter(Sponsers.user_id==id).first()
    print(id)
    print(sponser_id)
    print(sponser_id.user_id)
    campname=request.form["nameofcamp"]
    stime=request.form["startime"]
    dtime=request.form["endtime"]
    budg=request.form["budget"]
    visiblity=request.form["visiblity"]
    goals=request.form["goals"]
    description=request.form["description"]
    ans=db.session.query(user).get(id)
    campaign1=campaigns(sponser_id=sponser_id.user_id,
                        name=campname,
                        start_date=stime,
                        end_date=dtime,
                        budget=budg,
                        description=description,
                        Visibility=visiblity,
                        goals=goals)
    db.session.add(campaign1)
    db.session.commit()
    return redirect(f"/sponserhome/{id}")
    # return render_template("sponser_home.html",ans=ans)

@app.route("/sponserhome/<int:id>",methods=["GET"])
def sponser_login(id):
    ans=db.session.query(user).get(id)
    campdata=db.session.query(campaigns).filter(campaigns.sponser_id == id).all()
    print(len(campdata))
    return render_template("sponser_home.html",ans=ans,campdata=campdata)

@app.route("/update_camp_details/<int:campaigns_id>",methods=["GET"])
def some1(campaigns_id):
    data=db.session.query(campaigns).get(campaigns_id)
    print(data)
    return render_template("update_campdetails.html",data=data)

@app.route("/edit_campdetails/<int:campaigns_id>",methods=["GET","POST"])
def updatecamp(campaigns_id):
    if request.method=="GET":
        data=db.session.query(campaigns).get(campaigns_id)
        return render_template("update_campdetails.html",data=data)
    elif request.method=="POST":
        data=db.session.query(campaigns).get(campaigns_id)
        print(data.name)
        name=request.form["Name"]
        goals=request.form["Goals"]
        start_date=request.form["sdate"]
        end_date=request.form["edate"]
        budget=request.form["budget"]
        description=request.form["description"]
        data.name=name
        data.goals=goals
        data.start_date=start_date
        data.end_date=end_date
        data.budget=budget
        data.description=description
        db.session.commit()
        return redirect(f"/sponserhome/{data.sponser_id}")

@app.route("/delete_campagin/<int:campaigns_id>",methods=["GET"])
def delete(campaigns_id):
    data=db.session.query(campaigns).get(campaigns_id)
    id=data.sponser_id
    db.session.delete(data)
    db.session.commit()
    return redirect(f"/sponserhome/{id}")

@app.route("/sponserhome/campagins",methods=["GET"])
def details():
    data=db.session.query(campaigns).all()
    print(data.Visibility)
    return render_template("all_campdetails.html",data=data)

if __name__=="__main__":
    app.run(debug=True)