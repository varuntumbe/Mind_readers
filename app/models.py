from app import db,admin
from flask import redirect,url_for
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_security import RoleMixin, UserMixin,SQLAlchemyUserDatastore,current_user
from app.adminViewModels import *

#defining all my models

#------------------------------------------------------User-Role Model-------------------------------------

#association table
roles_users=db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Users(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    ans_part=db.relationship('FilQuestions',backref='psycologist_name',lazy='dynamic')
    roles=db.relationship(
        'Roles',
        secondary=roles_users,
        backref=db.backref('users',lazy='dynamic'),
        lazy='dynamic'
    )
    profile_info=db.relationship(
        'Profile',
        backref='user',
        uselist=False
    )

    def __repr__(self):
        return '<User : {}>'.format(self.email)

class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role : {}>'.format(self.name)




#-------------------------------------------------------------End of user-role Model---------------------------------------

#this model is only for admins
class UnfQuestions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    q_title=db.Column(db.String(100),nullable=False)
    q_desc=db.Column(db.String(300),nullable=False)
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<QuestionTitle {} >'.format(self.q_title)


#this model consists of filtered questions
class FilQuestions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    q_title=db.Column(db.String(100),nullable=False)
    q_desc=db.Column(db.String(300),nullable=False)
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    ans_text=db.Column(db.String(200),index=True)
    psy_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    no_upvotes=db.Column(db.Integer)  
    def __repr__(self):
        return '<QuestionTitle {} >'.format(self.q_title)

#this model is for psycologists
class Psycologists(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Psycologist: {} >'.format(self.username)


#this model is for profile for psycologists
class Profile(db.Model):
    psy_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(25))
    last_name=db.Column(db.String(25))
    about_me=db.Column(db.String(100))
    qualification=db.Column(db.String(50))
    phno=db.Column(db.Integer)
    address=db.Column(db.String(200))
    experiance=db.Column(db.String(150))
    education=db.Column(db.String(150))
    def __repr__(self):
        return '<profile: {} >'.format(self.name)       


#regestering perticular model to be only for admin
admin.add_view(AdminView(UnfQuestions,db.session))
admin.add_view(AdminView(Psycologists,db.session))
admin.add_view(AdminView(Users,db.session))
admin.add_view(AdminView(Roles,db.session))
