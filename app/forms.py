from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,IntegerField,PasswordField
from wtforms.validators import DataRequired,Length


#defining the first form (confession title)
class Confess(FlaskForm):
    conf_heading=StringField(label='Question',validators=[DataRequired(),Length(min=1,max=100)])
    conf_desc=TextAreaField(label='Describe',validators=[DataRequired(),Length(min=1,max=300)])
    submit=SubmitField(label='Submit')

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
    name=StringField(label='Name')
    about_me=TextAreaField(label='About Me')
    phno=IntegerField(label='Tel.phone')
    address=TextAreaField(label='Address')
    submit=SubmitField(label='Submit')