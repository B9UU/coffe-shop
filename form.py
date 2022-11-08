from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField,SelectField, IntegerField
from wtforms.validators import DataRequired,InputRequired

#login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
#register Form
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

# Add cafe

class AddCafe(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField('Map Url', validators=[DataRequired()])
    img_url = StringField('Image Url', validators=[DataRequired()])
    location = StringField("location", validators=[DataRequired()])
    has_sockets = SelectField('Sockets Number',choices=[(True, 'Yes'), (False, 'No')],validators=[InputRequired()])
    has_toilet = SelectField('Has Toilet',choices=[(True, 'Yes'), (False, 'No')],validators=[InputRequired()])
    has_wifi = SelectField('Has Wifi',choices=[(True, 'Yes'), (False, 'No')],validators=[InputRequired()])
    can_take_calls = SelectField('Can take calls',choices=[(True, 'Yes'), (False, 'No')],validators=[InputRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    coffee_price = StringField("coffee price", validators=[DataRequired()])
    submit = SubmitField("Add Caffe")