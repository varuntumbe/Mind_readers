from app import app,db,user_datastore
from flask import render_template,request,redirect,url_for
from app.forms import Confess,RegisterForm,AnswerForm,ProfileForm
from app.models import UnfQuestions,FilQuestions,Psycologists,Roles,Users,Profile
from datetime import datetime
from flask_security import login_required,current_user,roles_required
import random
import os
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash
from app.useful_func import get_last_record_psy_id

#home router
@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html')

@app.route('/confess',methods=['GET','POST'])
def conf():
    form=Confess()
    if form.validate_on_submit() and request.method=='POST':
        qh=form.conf_heading.data
        qdesc=form.conf_desc.data
        unfq_obj=UnfQuestions(q_title=qh,q_desc=qdesc)
        db.session.add(unfq_obj)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confess.html',form=form)

#handles adding specific record to safe db and removing from comman
@app.route('/addtodb/<pk>/<db_type>')
def add_to_db(pk,db_type):
    if db_type=='Unf Questions':
        unf_obj=UnfQuestions.query.filter(UnfQuestions.id==int(pk)).first()
        total=len(Users.query.all())+1
        # psy_id=int(random.randrange(start=1,stop=total))
        

        #getting the latest entry in database
        prev_psy_id=get_last_record_psy_id()

        #finding the next valid psy_id for this question
        pre_psy_id=(prev_psy_id+1)%total

        '''here we will assume that first 3 ids are admins in user table
        (another perfect work around is to check each time whether that psy_id is psycologist or not)'''
        if pre_psy_id>=0 and pre_psy_id<=3:
            pre_psy_id=4

        f_obj=FilQuestions(q_title=unf_obj.q_title,q_desc=unf_obj.q_desc,psy_id=pre_psy_id,no_upvotes=0)
        db.session.add(f_obj)
        db.session.commit()
        db.session.delete(unf_obj)
        db.session.commit()
    else:
        psy=Psycologists.query.filter(Psycologists.id==pk).first()
        user=user_datastore.create_user(email=psy.email,password=psy.password)
        db.session.add(user)
        db.session.commit()
        role=Roles.query.filter(Roles.id==2).first()
        re=user_datastore.add_role_to_user(user,role)
        db.session.commit()
        #setting up their profile also ----------------some bug about unique constraint
        psy_id=Users.query.filter(Users.email==psy.email).first().id
        pr=Profile(psy_id=psy_id,id=psy_id)
        db.session.add(pr)
        db.session.commit()
        if re:
            db.session.delete(psy)
            db.session.commit()
            return 'Data has been moved'
        else:
            return 'unsuccessful'

    return redirect(url_for('conf'))

#handles registration
@app.route('/reg',methods=['GET','POST'])
def reg():
    form=RegisterForm()
    if request.method == 'POST':
        f = request.files['file']
        # print(f.filename)
        f.save(os.path.join(app.instance_path, 'files', secure_filename(f.filename)))
        psy_name=form.email.data
        psy_password=form.password.data
        psy=Psycologists(email=psy_name,password=psy_password)
        db.session.add(psy)
        db.session.commit()
        return 'Thank You for your Rgeistrations!!'
    return render_template('register.html',form=form)

#shows all the questions
@app.route('/questions')
def questions():
    page = request.args.get('page', type=int, default=1)
    all_quest=FilQuestions.query.paginate(page,app.config['POST_PER_PAGE'],False)
    prev_url=next_url=None
    if all_quest.has_next:
        next_url=url_for('questions',page=all_quest.next_num)
    if all_quest.has_prev:
        prev_url=url_for('questions',page=all_quest.prev_num)

    return render_template('questions.html',questions=all_quest.items,next_url=next_url,prev_url=prev_url)

#next route is for answer
@app.route('/answer',methods=['GET','POST'])
@roles_required('psycologist')
def answers():
    form=AnswerForm()
    if form.validate_on_submit and request.method=='POST':
        q_id=request.args.get('q_id')
        q_obj=FilQuestions.query.filter(FilQuestions.id==q_id).first()
        q_obj.ans_text=form.answer.data
        db.session.commit()
        return redirect(url_for('answers'))

    all_quest=current_user.ans_part.all()
    print(all_quest)
    return render_template('que_to_be_ansd.html',form=form,questions=all_quest)

#next route is for set_profile
@app.route('/edit_profile/<p_id>',methods=['GET','POST'])
@roles_required('psycologist')
def setprofile(p_id):
    #simple security fix
    if int(p_id) != current_user.id:
        return redirect(url_for('index'))

    form=ProfileForm()                                    #----------------------------Bug is there-------------------------------------#
    user_id=current_user.id
    cur_user=Profile.query.filter(Profile.id==user_id).first()
    if form.validate_on_submit and request.method=='POST':
        pr_obj=Profile.query.filter(Profile.id==current_user.id).first()
        if form.first_name.data is not None:
            pr_obj.first_name=form.first_name.data

        if form.last_name.data is not None:
            pr_obj.last_name=form.last_name.data

        if form.about_me.data is not None:
            pr_obj.about_me=form.about_me.data

        if form.phno.data is not None:
            pr_obj.phno=form.phno.data

        if form.qual.data is not None:
            pr_obj.qualification=form.qual.data

        if form.address.data is not None:
            pr_obj.address=form.address.data

        if form.experiance.data is not None:
            pr_obj.experiance=form.experiance.data

        if form.education.data is not None:
            pr_obj.education=form.education.data

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_profile.html',form=form,cur_user=cur_user)

#next route is for view Profile
@app.route('/view_profile')
def viewprofile():
    p_id=request.args.get('psy_id')
    my_info=Profile.query.filter(Profile.id==p_id).first()
    return render_template('view_profile.html',my_info=my_info)
