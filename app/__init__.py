from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
from flask_security import Security,SQLAlchemyUserDatastore
from app.adminViewModels import HomeAdminView
from werkzeug import secure_filename
import os

#initializing flask app instance
app=Flask(__name__)
app.config.from_object(Config)
os.makedirs(os.path.join(app.instance_path, 'files'), exist_ok=True)
# os.makedirs(os.path.join(app.instance_path, 'profile_pics'), exist_ok=True)
#Bootstrap instance
Bootstrap(app)

#database instance
db=SQLAlchemy(app)

#migrate instance
migrate=Migrate(app,db,render_as_batch=True)


#Admin instance
admin=Admin(app,'FlaskApp',url='/',index_view=HomeAdminView(name='Home'))


from app.models import *
#Flask-security
user_datastore = SQLAlchemyUserDatastore(db,Users,Roles)
securtiy=Security(app,user_datastore)

from app import routes,models



