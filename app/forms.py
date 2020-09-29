from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,IntegerField,PasswordField
from wtforms.validators import DataRequired,Length


#defining the first form (confession title)
class Confess(FlaskForm):
    conf_heading=TextAreaField(label='Problem/Question',validators=[DataRequired(),Length(min=1,max=100)])
    conf_desc=TextAreaField(label='Tell us more',validators=[DataRequired(),Length(min=1,max=300)])

#Registration Form
class RegisterForm(FlaskForm):
    email=StringField(label='Email',validators=[DataRequired(),Length(min=1,max=100)])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='submit')

#answe form
class AnswerForm(FlaskForm):
    answer=TextAreaField(label='Write Ans',validators=[DataRequired(),Length(min=10,max=200)])
    submit=SubmitField(label='Submit')

#profile Form
class ProfileForm(FlaskForm):
    first_name=StringField(label='First Name')
    last_name=StringField(label='Last Name')
    about_me=TextAreaField(label='A few words about yourself')
    qual=StringField(label='Qualifications')
    phno=IntegerField(label='Telephone No ')
    address=TextAreaField(label='Address')
    experiance=TextAreaField(label='Experiance')
    education=TextAreaField(label='Education')
