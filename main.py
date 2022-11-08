from flask import Flask,render_template,flash,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from form import LoginForm, RegisterForm,AddCafe
from flask_login import LoginManager,login_user,current_user,UserMixin,logout_user,login_required
import os

login_manager = LoginManager()
#ini flask app and database
app = Flask(__name__)
app.app_context().push()
db = SQLAlchemy()
Bootstrap(app)
# configure the SQLite database, relative to the app instance folder
##CONNECT TO DB
uri = os.environ.get("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config['SECRET_KEY'] = os.environ.get('SECRET')
# initialize the app with the extension
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# caffe table
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    has_sockets = db.Column(db.BOOLEAN, nullable=False)
    has_toilet = db.Column(db.BOOLEAN, nullable=False)
    has_wifi = db.Column(db.BOOLEAN, nullable=False)
    can_take_calls = db.Column(db.BOOLEAN, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.Integer, nullable=False)

# users table 
class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
db.create_all()

# home displaying all caffes in the data base
@app.route('/')
def home():
    data = db.session.query(Cafe).all()
    return render_template('index.html',cafes = data,user=current_user)

#login endpoint
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter_by(email=form.email.data).first()
        if user:
            passwo = check_password_hash(user.password,form.password.data)
            if passwo:
                flash('youre in')
                login_user(user)
                return redirect(url_for('home'))
        
        flash('credential incorrect try again or register')
        return redirect(url_for('login'))
        
    return render_template('login.html',form=form,user=current_user)

# register endpoint
@app.route('/register', methods=['GET','POST'])
def register():
    # add account into the table if form validated
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter_by(email=form.email.data).first()
        if not user:
            use= Users(
                email = form.email.data,
                name = form.name.data,
                password= generate_password_hash(form.password.data,
                method='pbkdf2:sha256',salt_length=8),
            )
            db.session.add(use)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('email all ready has an account try to login or register with another email')
            return redirect(url_for('login'))


    return render_template('register.html',form=form,user=current_user)

# add cafe endpoint
@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():

    # redirect to login page if user not loged in
    if not current_user.is_authenticated:
        flash('you have to login to add a caffe')
        return redirect(url_for('login'))

    # add form into data base if validated  
    form = AddCafe()
    if form.validate_on_submit():
        print(type(bool(form.has_toilet.data)))
        cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = bool(form.has_sockets.data),
            has_toilet = bool(form.has_toilet.data),
            has_wifi = bool(form.has_wifi.data),
            can_take_calls =bool(form.can_take_calls.data), 
            seats = form.seats.data,
            coffee_price = form.coffee_price.data,
        )
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('login.html',form=form,user=current_user)
# logout the user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)