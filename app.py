from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import jinja2,os
from werkzeug.utils import secure_filename
api=None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3" 
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key = '123456789Anmol'

# defining models
Active=0

class user(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String, unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String) 
    flagged_user=db.Column(db.Boolean, default=False)  

class influencer(db.Model):
    __tablename__='influcener'
    influencer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,db.ForeignKey(user.username))
    Category=db.Column(db.String)
    Niche=db.Column(db.String)
    reach=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey(user.user_id))
    photo_path = db.Column(db.String)
    flagged_info=db.Column(db.Boolean, default=False)

class Sponsers(db.Model):
    __tablename__='sponsers'
    Sponsers_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Company_name=db.Column(db.String)
    industry=db.Column(db.String)
    budget=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey(user.user_id))
    flagged_spons=db.Column(db.Boolean, default=False)
    
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
    flagged_camp=db.Column(db.Boolean, default=False)

class Ad_request(db.Model):
    __tablename__="ad_req"
    adreq_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    campaigns_id=db.Column(db.Integer,db.ForeignKey(campaigns.campaigns_id))
    sponsers_id=db.Column(db.Integer,db.ForeignKey(Sponsers.Sponsers_id))
    messages=db.Column(db.String)
    requirements=db.Column(db.String)
    payment_amount=db.Column(db.String)
    status=db.Column(db.String)
    Influ_id=db.Column(db.Integer,db.ForeignKey(influencer.influencer_id))
    flagged_ad_reqd=db.Column(db.Boolean, default=False)

#basic logging
def countsss(x):
    count=0
    for i in x:
        count+=1
    return count    


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
            campdata=db.session.query(campaigns).all()
            infudata=db.session.query(influencer).all()
            addata=db.session.query(Ad_request).all()
            spon_data=db.session.query(Sponsers).all()
            money=0
            for i in addata:
                money+=int(i.payment_amount)
            print(money)
            user_count=countsss(data)
            camp_count=countsss(campdata)
            infu_count=countsss(infudata)
            adcount=countsss(addata)
            spons_count=countsss(spon_data)
            # for i in data:
            #     user_count+=1
            return render_template('admin.html',money=money,
                                   data=data,
                                   user_count=user_count,
                                   camp_count=camp_count,infu_count=infu_count,adcount=adcount,spons_count=spons_count)
        else:
            return render_template('Notadmin.html')
    elif role=="Sponsers":
        #write code for the who had already registerd
        if ans==None or passs==None:
            return render_template("Notregistered.html")
        elif ans.username==use2 and ans.password==password and ans.role==role:
            id=ans.user_id
            return redirect(f"/sponserhome/{id}")
            # return render_template("sponser_home.html",ans=ans)
        else:
            return render_template("Notregistered.html")
    else:
        if ans==None or passs==None:
            return render_template("Notregistered.html")
        elif ans.username==use2 and ans.password==password and ans.role==role:
            id=ans.user_id
            return redirect(f"/userlogin/{id}")
        else:
            return render_template("Notregistered.html")

@app.route("/userlogin/<int:id>",methods=["GET"])        
def userlogin(id):
    user1=db.session.query(influencer).filter(influencer.user_id == id).first() 
    addata=db.session.query(Ad_request).filter(Ad_request.Influ_id==user1.influencer_id).all()
    print(addata==[])
    desh=[]
    count=0
    Money=0
    if addata != []:
        for i in addata:
            k=i.sponsers_id
            campdata=db.session.query(campaigns).filter(campaigns.campaigns_id==i.campaigns_id).first()
            spons=db.session.query(Sponsers).filter(Sponsers.Sponsers_id == k).first()
            ifudata=db.session.query(influencer).filter(influencer.influencer_id==i.Influ_id).first()
            print(ifudata)
            l=[]
            l.append(count)
            l.append(spons.Company_name)
            l.append(i.payment_amount)
            Money+=int(i.payment_amount)
            print(campdata.name)
            l.append(i.status)
            l.append(i.adreq_id)
            l.append(campdata.name)
            desh.append(l)
            count+=1
        return render_template("user.html",user1=user1,desh=desh,Money=Money,infu_id=ifudata.influencer_id)
    else:
        return render_template("user.html",user1=user1,desh=desh,Money=Money)
@app.route("/sponserhome/<int:id>",methods=["GET"])
def sponser_login(id):
    ans=db.session.query(user).get(id)
    sponsdata=db.session.query(Sponsers).filter(Sponsers.user_id==id).first()
    campdata=db.session.query(campaigns).filter(campaigns.sponser_id == sponsdata.Sponsers_id).all()
    adddata=db.session.query(Ad_request).filter(Ad_request.sponsers_id == sponsdata.Sponsers_id).all()
    flag=True
    din=dict()
    count=1000
    for i in adddata:
        sponsdata1=db.session.query(influencer).filter(influencer.influencer_id==i.Influ_id).first()
        userdata=db.session.query(user).filter(user.user_id==sponsdata1.user_id).first()
        print(userdata)
        din[count]=[i.payment_amount,i.messages,i.requirements,i.status,i.adreq_id,userdata.username,]
        count+=1
    print(din)    
    return render_template("sponser_home.html",ans=ans,campdata=campdata,din=din,flag=flag,sponsdata=sponsdata.Sponsers_id)

#register

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
    photo = request.files['photo']
    nuser=user(username=user1,password=pass1,role=role1)
    db.session.add(nuser)
    if photo:
        filename = secure_filename(photo.filename)
        print(filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo_path = photo_path.replace('\\', '/')
        photo.save(photo_path)
        photo_path = filename
    else:
        photo_path = None
    db.session.commit()
    users=db.session.query(user).filter(user.username==user1).first()
    info1=influencer(name=naam,
                     Category=Cate,
                     Niche=Niche,
                     reach=reach,
                     user_id=users.user_id,
                     photo_path=photo_path)
    db.session.add(info1)
    db.session.commit()
    id=users.user_id
    flash('You have been successfully registered! please logg in ')    
    return render_template("logging.html")



#admin files
    
@app.route("/login",methods=['GET'])
def loginadmin():
    
    data=db.session.query(user).all()
    campdata=db.session.query(campaigns).all()
    infudata=db.session.query(influencer).all()
    addata=db.session.query(Ad_request).all()
    spon_data=db.session.query(Sponsers).all()
    user_count=countsss(data)
    camp_count=countsss(campdata)
    infu_count=countsss(infudata)
    adcount=countsss(addata)
    money=0
    spons_count=countsss(spon_data)
    for i in addata:
        money+=int(i.payment_amount)
    print(money)
    return render_template('admin.html',money=money,
                            data=data,
                            user_count=user_count,camp_count=camp_count,infu_count=infu_count,adcount=adcount,spons_count=spons_count)

@app.route("/login_users",methods=["GET"])
def loginuser():
    det=db.session.query(user).filter(user.username==user.username).all()
    return render_template('admin_user.html',details=det)

@app.route("/login_users/flag",methods=["GET"])
def loginuser_flag():
    det=db.session.query(user).filter(user.username==user.username).all()
    return render_template('admin_flaguser1.html',details=det)

@app.route("/login_camp",methods=["GET"])
def logincamp():
    campdata=db.session.query(campaigns).all()
    campdata_need=None
    return render_template('admin_camp.html',campdata=campdata,campdata_need=campdata_need)

@app.route("/admin_spons",methods=["GET"])
def loginspons():
    sponsdata=db.session.query(Sponsers).all()
    spons1=None 
    return render_template("admin_sponsers.html",sponsdata=sponsdata,spons1=spons1)

@app.route("/admin_spons_flag/<spons_id>",methods=["GET"])
def admin_spons_flag(spons_id):
    sponsdata=db.session.query(Sponsers).all()
    spons1=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==spons_id).first()
    spons1.flagged_spons=True
    db.session.commit()
    return  render_template("admin_sponsers.html",sponsdata=sponsdata,spons1=spons1)

@app.route("/admin_spons_flag_true/<spons_id>",methods=["GET"])
def admin_spons_flag1(spons_id):
    sponsdata=db.session.query(Sponsers).all()
    spons1=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==spons_id).first()
    spons1.flagged_spons=False
    db.session.commit()
    return  render_template("admin_sponsers.html",sponsdata=sponsdata,spons1=spons1)

@app.route("/admin_user_flag/<user_id>",methods=["GET"])
def admin_user_flag(user_id):
    details=db.session.query(user).all()
    user1=db.session.query(user).filter(user.user_id==user_id).first()
    user1.flagged_user=True
    db.session.commit()
    return  render_template("admin_user.html",details=details)

@app.route("/admin_user_flag_true/<user_id>",methods=["GET"])
def admin_user_flag12(user_id):
    details=db.session.query(user).all()
    user1=db.session.query(user).filter(user.user_id==user_id).first()
    user1.flagged_user=False    
    db.session.commit()
    return  render_template("admin_user.html",details=details)

@app.route("/admin_camp/<int:camp_id>",methods=["GET"])
def admin_camp(camp_id):
    campdata=db.session.query(campaigns).all()
    campdata_need=db.session.query(campaigns).filter(campaigns.campaigns_id==camp_id).first()
    return render_template('admin_camp.html',campdata=campdata,campdata_need=campdata_need)

@app.route("/admin_camp_flag/<int:camp_id>",methods=["GET"])
def admin_camp_flag(camp_id):
    campdata=db.session.query(campaigns).all()
    campdata_need=db.session.query(campaigns).filter(campaigns.campaigns_id==camp_id).first()
    campdata_need.flagged_camp=True
    db.session.commit()
    return render_template('admin_camp.html',campdata=campdata,campdata_need=campdata_need)

@app.route("/admin_camp_flag_true/<int:camp_id>",methods=["GET"])
def admin_camp_flag122(camp_id):
    campdata=db.session.query(campaigns).all()
    campdata_need=db.session.query(campaigns).filter(campaigns.campaigns_id==camp_id).first()
    campdata_need.flagged_camp=False
    db.session.commit()
    return render_template('admin_camp.html',campdata=campdata,campdata_need=campdata_need)

@app.route("/admin_spons/<int:spons_id>",methods=["GET"])
def admin_spons(spons_id):
    sponsdata=db.session.query(Sponsers).all()
    spons1=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==spons_id).first()
    return render_template("admin_sponsers.html",sponsdata=sponsdata,spons1=spons1)

@app.route("/admin_info",methods=["GET"])
def admin_info():
    infodata=db.session.query(influencer).all()
    info12=None
    return render_template("admin_info.html",infodata=infodata,info12=info12)

@app.route("/admin_info/<int:info_id>",methods={"GET"})
def admin_info1(info_id):
    infodata=db.session.query(influencer).all()
    info12=db.session.query(influencer).filter(influencer.influencer_id==info_id).first()
    return render_template("admin_info.html",infodata=infodata,info12=info12)

@app.route("/admin_info_flag/<int:info_id>",methods=["GET"])
def info_flag(info_id):
    infodata=db.session.query(influencer).all()
    info12=db.session.query(influencer).filter(influencer.influencer_id==info_id).first()
    info12.flagged_info=True
    db.session.commit()
    return render_template("admin_info.html",infodata=infodata,info12=info12)

@app.route("/admin_info_flag_false/<int:info_id>",methods=["GET"])
def info_flag11(info_id):
    infodata=db.session.query(influencer).all()
    info12=db.session.query(influencer).filter(influencer.influencer_id==info_id).first()
    info12.flagged_info=False
    db.session.commit()
    return render_template("admin_info.html",infodata=infodata,info12=info12)


@app.route("/admin_adreq",methods=["GET"])
def admin_adreq():
    addata=db.session.query(Ad_request).all()
    data=dict()
    count=1
    for i in addata:
        sponser=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==i.sponsers_id).first()
        company=db.session.query(campaigns).filter(campaigns.campaigns_id==i.campaigns_id).first()
        data[count]=[i.adreq_id,sponser.Company_name,company.name,i.status,i.flagged_ad_reqd]
        count+=1
    print(data)    
    return render_template("admin_adreq.html",addata=addata,data=data)

@app.route("/admin_ad_flag/<int:adreq_id>",methods=["GET"])
def adreq_flag(adreq_id):
    addata=db.session.query(Ad_request).all()
    add1=db.session.query(Ad_request).filter(Ad_request.adreq_id==adreq_id).first()
    add1.flagged_ad_reqd=True
    db.session.commit()
    data=dict()
    count=1
    for i in addata:
        sponser=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==i.sponsers_id).first()
        company=db.session.query(campaigns).filter(campaigns.campaigns_id==i.campaigns_id).first()
        data[count]=[i.adreq_id,sponser.Company_name,company.name,i.status,i.flagged_ad_reqd]
        count+=1
    print(data)    
    return render_template("admin_adreq.html",addata=addata,data=data)

@app.route("/admin_ad_flag_true/<int:adreq_id>",methods=["GET"])
def adreq_flag12(adreq_id):
    addata=db.session.query(Ad_request).all()
    add1=db.session.query(Ad_request).filter(Ad_request.adreq_id==adreq_id).first()
    add1.flagged_ad_reqd=False
    db.session.commit()
    data=dict()
    count=1
    for i in addata:
        sponser=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==i.sponsers_id).first()
        company=db.session.query(campaigns).filter(campaigns.campaigns_id==i.campaigns_id).first()
        data[count]=[i.adreq_id,sponser.Company_name,company.name,i.status,i.flagged_ad_reqd]
        count+=1
    print(data)    
    return render_template("admin_adreq.html",addata=addata,data=data)

@app.route("/login_camp/flag",methods=["GET"])
def logincampflag():
    campdata=db.session.query(campaigns).all()
    campdata_need=None
    return render_template('admin_flagcamp.html',campdata=campdata,campdata_need=campdata_need)

@app.route("/login_spons/flag",methods=["GET"])
def loginsponsflag():
    sponsdata=db.session.query(Sponsers).all()
    spons1=None 
    return render_template("admin_flagspon.html",sponsdata=sponsdata,spons1=spons1)

@app.route("/admin_info/flag",methods=["GET"])
def admin_infoflag():
    infodata=db.session.query(influencer).all()
    info12=None
    return render_template("admin_flaguser.html",infodata=infodata,info12=info12)

@app.route("/admin_adreq/flag",methods=["GET"])
def admin_adreq_flag():
    addata=db.session.query(Ad_request).all()
    data=dict()
    count=1
    for i in addata:
        sponser=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==i.sponsers_id).first()
        company=db.session.query(campaigns).filter(campaigns.campaigns_id==i.campaigns_id).first()
        data[count]=[i.adreq_id,sponser.Company_name,company.name,i.status,i.flagged_ad_reqd]
        count+=1
    print(data)    
    return render_template("admin_flagadreq.html",addata=addata,data=data)

#sponser files

@app.route("/create_camp/<int:user_id>")
def start(user_id):
    user2 = db.session.query(user).get(user_id)
    iduser=user_id

    return render_template("addcamp.html",user2=user2)

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
        data.Visibility=request.form["visiblity"]
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
    adddata=db.session.query(Ad_request).filter(Ad_request.campaigns_id==campaigns_id).all()
    id=data.sponser_id
    db.session.delete(adddata)
    db.session.delete(data)
    db.session.commit()
    return redirect(f"/sponserhome/{id}")

@app.route("/sponserhome/campagins",methods=["GET"])
def details():
    data=db.session.query(campaigns).all()
    return render_template("all_campdetails.html",data=data)

@app.route("/sponser_home/find/<int:id>",methods=["GET"])
def homelander(id):
    userdata1=dict()
    ans=db.session.query(user).filter(user.role=='user').all()
    for i in ans:
        k=i.user_id
        l=[]
        name=i.username
        userdata=db.session.query(influencer).filter(influencer.user_id==k).first()
        l.append(k)
        l.append(userdata.reach)
        userdata1[name]=l
    return render_template("sponser_user_find.html",userdata1=userdata1,id=id)

@app.route("/sponser_home/value/<int:id>",methods=["POST"])
def vought(id):
    value=request.form["value"]
    data=db.session.query(user).filter(user.username==value).first()
    userdata=db.session.query(influencer).filter(influencer.user_id==data.user_id).first()
    if data.role=="user":
        ans=data
    else:
        ans=None    
    return render_template("sponser_user_find1.html",id=id,ans=ans,userdata=userdata)

#find campagins as sponsers

@app.route("/user_home/Campagin/<int:id>",methods=["GET","POST"])
def find_camp(id):
    user1=db.session.query(influencer).filter(influencer.influencer_id==id).first()
    if request.method=="GET":
        campdata=db.session.query(campaigns).all()
        count=1
        l=dict()
        for i in campdata:
            if i.Visibility!="hidden":
                l[count]=[i.name,i.start_date,i.end_date,i.campaigns_id]
                count+=1
        print(l)        
        return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
    elif request.method=="POST":
        name=request.form["name"]
        budget=request.form["budget"]
        if len(name)==0:
            name=None
        print(name==None)    
        try:
            budget=int(budget)
        except ValueError:
            budget=None
        if  budget==None and name==None:
            i=db.session.query(campaigns).filter(campaigns.name==name).first()
            count=1
            l=dict()
            if i is None:
                l=None
                return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
            if i.Visibility!="hidden":
                l[count]=[i.name,i.start_date,i.end_date,i.campaigns_id]
            else:
                l=None    
            return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
        elif name==None:
            campdata1=db.session.query(campaigns).filter(campaigns.budget==budget).all()
            count=1
            l=dict()
            for i in campdata1:
                print(i)
                if i is None:
                    l=None
                    return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
                if i.Visibility!="hidden" and i.budget==int(budget):
                    l[count]=[i.name,i.start_date,i.end_date,i.campaigns_id]
                    count+=1
                else:
                    l=None    
            return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
        elif (budget==None):
            campdata2=db.session.query(campaigns).filter(campaigns.name==name).all()
            count=1
            l=dict()
            for i in campdata2:
                if i is None:
                    l=None
                    return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
                if i.Visibility!="hidden":
                    l[count]=[i.name,i.start_date,i.end_date,i.campaigns_id]
                    count+=1
                else:
                    l=None    
            return render_template("camp_find.html",l=l,id=id,user_id=user1.user_id)
        else:
            campdata2=db.session.query(campaigns).filter(campaigns.name==name).all()
            count=1
            l=dict()
            for i in campdata2:
                if i is None:
                    l=None
                    return render_template("camp_find.html",l=l,id=id)
                if i.Visibility!="hidden" and i.budget==budget:
                    l[count]=[i.name,i.start_date,i.end_date,i.campaigns_id]
                    count+=1
                else:
                    l=None    
            return render_template("camp_find.html",l=l,id=id)

@app.route("/sponser/request/<int:id>",methods=["GET"])
def adreq(id):
    print(id)
    data=db.session.query(influencer).filter(influencer.user_id==id).first()
    return render_template("ad_user.html",data=data,id=id)

@app.route("/sponser/adreq_sent/<int:userid>",methods=["GET"])
def sent(userid):
    l=[]
    user_Data=db.session.query(influencer).filter(influencer.user_id==userid).first()
    campdata=db.session.query(campaigns).all()
    for data in campdata:
        if data.Visibility=="visible":
            l.append(data)
    print(l)               
    return render_template("add_req.html",l=l,user_Data=user_Data)

@app.route("/sponser/adreq_sent/<int:id>",methods=["POST"])    
def post(id):
    camp=request.form["camp"]
    info_name=request.form["userName"]
    Payment=request.form["Payment"]
    message=request.form["message"]
    requirements=request.form["req"]
    campdata=db.session.query(campaigns).filter(campaigns.campaigns_id==camp).first()
    sponsdata=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==campdata.sponser_id).first()
    print(campdata)
    status='Pending'        
    ad1=Ad_request(campaigns_id=camp,sponsers_id=campdata.sponser_id,
                   requirements=requirements,
                   messages=message,payment_amount=Payment,status=status,Influ_id=id)
    db.session.add(ad1)
    db.session.commit()
    return redirect (f"/sponserhome/{sponsdata.user_id}")

@app.route("/adreq/accept/<int:adreq_id>",methods=["GET"])
def accept(adreq_id):
    adddata=db.session.query(Ad_request).filter(Ad_request.adreq_id==adreq_id).first()
    adddata.status="Accepted"
    db.session.commit()
    sponsdata=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==adddata.sponsers_id).first()
    print('done')
    return redirect (f"/sponserhome/{sponsdata.user_id}")

@app.route("/user/view/<int:id>/<cname>/<int:money>",methods=["GET"])
def deatails(id,cname,money):
    data=db.session.query(Ad_request).filter(Ad_request.adreq_id==id).first()
    return render_template("user_sponser_det.html",data=data,cname=cname,money=money,id=id)

@app.route("/view/user/reject/<int:id>",methods=["GET"])
def reject(id):
    addata=db.session.query(Ad_request).filter(Ad_request.adreq_id==id).first()
    sponsdata=db.session.query(influencer).filter(influencer.influencer_id==addata.Influ_id).first()
    userdata=db.session.query(user).filter(user.user_id==sponsdata.user_id).first()
    print(userdata.username)
    addata.status="Rejected"
    db.session.commit()
    return redirect (f"/userlogin/{userdata.user_id}")

@app.route("/view/user/modify/<int:id>",methods=["GET","POST"])
def deliver(id):
    if request.method=="GET":
        addata=db.session.query(Ad_request).filter(Ad_request.adreq_id==id).first()
        sponsdata=db.session.query(influencer).filter(influencer.influencer_id==addata.Influ_id).first()
        userdata=db.session.query(user).filter(user.user_id==sponsdata.user_id).first()
        return render_template("adreq_modify.html",addata=addata)
    elif request.method=="POST":
        addata=db.session.query(Ad_request).filter(Ad_request.adreq_id==id).first()
        addata.payment_amount=request.form["Money"]
        addata.messages=request.form["message"]
        addata.requirements=request.form["req"]
        addata.status="Modified"
        db.session.commit()
        sponsdata=db.session.query(influencer).filter(influencer.influencer_id==addata.Influ_id).first()
        userdata=db.session.query(user).filter(user.user_id==sponsdata.user_id).first()
        return redirect (f"/userlogin/{userdata.user_id}")

@app.route("/view/user/Accept/<int:ad_id>",methods=["GET"])
def accepted(ad_id):
    add=db.session.query(Ad_request).filter(Ad_request.adreq_id==ad_id).first()
    sponsdata=db.session.query(influencer).filter(influencer.influencer_id==add.Influ_id).first()
    userdata=db.session.query(user).filter(user.user_id==sponsdata.user_id).first()
    add.status="Accepted"
    db.session.commit()
    return redirect (f"/userlogin/{userdata.user_id}")

@app.route("/view/Sponser/reject/<int:id>",methods=["GET"])
def rejct_spons(ad_id):
    add=db.session.query(Ad_request).filter(Ad_request.adreq_id==ad_id).first()
    sponsdata=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==add.sponsers_id).first()
    add.status="Rejected"
    db.session.commit()
    return redirect (f"/sponserhome/{sponsdata.user_id}")

@app.route("/view/Sponser/Accept/<ad_id>",methods=["GET"])
def accept_spons(ad_id):
    add=db.session.query(Ad_request).filter(Ad_request.adreq_id==ad_id).first()
    sponsdata=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==add.sponsers_id).first()
    add.status="Accepted"
    db.session.commit()
    return redirect (f"/sponserhome/{sponsdata.user_id}")

@app.route("/view/Sponser/cancel/<ad_id>",methods=["GET"])
def cancel_req(ad_id):
    add=db.session.query(Ad_request).filter(Ad_request.adreq_id==ad_id).first()
    sponsdata=db.session.query(Sponsers).filter(Sponsers.Sponsers_id==add.sponsers_id).first()
    db.session.delete(add)
    db.session.commit()
    return redirect (f"/sponserhome/{sponsdata.user_id}") 

@app.route("/userdetails/update/<infl_id>",methods=["GET","POST"])
def user_update(infl_id):
    if request.method=="GET":
        data=db.session.query(influencer).filter(influencer.influencer_id==infl_id).first()
        
        return render_template("update_profile.html",data=data,infl_id=infl_id)
    elif request.method=="POST":
        data=db.session.query(influencer).filter(influencer.influencer_id==infl_id).first()
        data.name=request.form["vname"]
        data.Niche=request.form["niche"]
        data.Category=request.form["cate"]
        data.reach=request.form["follows"]
        photo=request.files["photo"]
        if photo:
            filename = secure_filename(photo.filename)
            print(filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_path = photo_path.replace('\\', '/')
            photo.save(photo_path)
            photo_path = filename
            data.photo_path=photo_path
        else:
            photo_path = None
        db.session.commit()
        return redirect(f"/userlogin/{data.user_id}")


@app.route("/user/<int:camp_id>/<int:info_id>",methods=["GET","POST"])
def req_use(camp_id,info_id):
    if request.method=="GET":
        campdata=db.session.query(campaigns).filter(campaigns.campaigns_id==camp_id).first()
        userdata=db.session.query(influencer).filter(influencer.influencer_id==info_id).first()
        return render_template("user_adre.html",camp_id=camp_id,info_id=info_id,userdata=userdata,campdata=campdata)
    else:
        name=request.form["Name12"]
        payment=request.form["Payment"]
        message=request.form["message"]
        terms=request.form["req"]
        campdata=db.session.query(campaigns).filter(campaigns.campaigns_id==camp_id).first()
        addq=Ad_request(campaigns_id=camp_id,sponsers_id=campdata.sponser_id,
                   requirements=terms,
                   messages=message,payment_amount=payment,status="Modified",Influ_id=info_id,flagged_ad_reqd=False)
        db.session.add(addq)
        db.session.commit()
        user11=db.session.query(influencer).filter(influencer.influencer_id==info_id).first()
        return redirect(f"/userlogin/{user11.user_id}")

#stats

@app.route("/user/stats/<int:userid>",methods=["GET","POST"])
def stats(userid):
    data=db.session.query(user).all()
    campdata=db.session.query(campaigns).all()
    infudata=db.session.query(influencer).all()
    addata=db.session.query(Ad_request).all()
    spon_data=db.session.query(Sponsers).all()
    money=0
    for i in addata:
        money+=int(i.payment_amount)
    print(money)
    user_count=countsss(data)
    camp_count=countsss(campdata)
    infu_count=countsss(infudata)
    adcount=countsss(addata)
    spons_count=countsss(spon_data)
    suser_id=None
    return render_template("stats.html",money=money,
                            user_count=user_count,
                            camp_count=camp_count,suser_id=suser_id,infu_count=infu_count,adcount=adcount,spons_count=spons_count,userid=userid)

@app.route("/user/home/<int:userid>",methods=["GET"])
def user_home1(userid):
    return redirect(f"/userlogin/{userid}")

@app.route("/sponser/stats/<int:suser_id>",methods=["GET","POST"])
def stats1(suser_id):
    data=db.session.query(user).all()
    campdata=db.session.query(campaigns).all()
    infudata=db.session.query(influencer).all()
    addata=db.session.query(Ad_request).all()
    spon_data=db.session.query(Sponsers).all()
    money=0
    for i in addata:
        money+=int(i.payment_amount)
    print(money)
    user_count=countsss(data)
    camp_count=countsss(campdata)
    infu_count=countsss(infudata)
    adcount=countsss(addata)
    spons_count=countsss(spon_data)
    userid=None
    return render_template("stats.html",money=money,suser_id=suser_id,
                            user_count=user_count,
                            camp_count=camp_count,infu_count=infu_count,adcount=adcount,spons_count=spons_count,userid=userid)

@app.route("/sponser/home/<int:suserid>",methods=["GET"])
def user_home11(suserid):
    return redirect(f"/sponserhome//{suserid}")

if __name__=="__main__":
    app.run(debug=True)