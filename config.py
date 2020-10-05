import os

basepath= os.path.abspath(os.path.dirname(__name__))

class Config(object):
    DEBUG=True
    SECRET_KEY='this_is_secret'
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basepath,'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    FLASK_ADMIN_SWATCH = 'cyborg'
    SECURITY_PASSWORD_SALT='saltsaltsalty'
    SECURITY_PASSWORD_HASH='sha512_crypt'
    POST_PER_PAGE= 5
