from flask import Flask, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy.testing import db
from forms import RegistrationForm
from forms import LoginForm
from flask_principal import identity_loaded, Principal, Permission, RoleNeed, UserNeed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1b2c3d4e5f6'  # replace with a real secret key
bcrypt = Bcrypt(app)


#Initialize flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # route to redirect unauthorized users


# Initialize flask principal
Principal(app)
admin_permission = Permission(RoleNeed('admin'))


# Define Permissions
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


# Load the user when logged in
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if not hasattr(current_user, 'id'):
        return  # Skip if user isn’t logged in

    # Add user ID to identity
    identity.provides.add(UserNeed(current_user.id))

    # Add roles to identity
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

    # Debugging: Print the identity’s needs
    print("Identity provides:", identity.provides)  # Check console output


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return "Hello World"


@app.route("/dashboard")
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html",tickets=tickets)


@app.route("/create_ticket", methods=["POST"])
@login_required
def create_ticket():
    if request.form['submit']:
        title = request.form['title']
        description = request.form["description"]
        new_ticket = Ticket(title=title,description=description, user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()
        message = f" the title is {title} and description is {description}"
    return redirect('/dashboard')


@app.route('/update_status/<int:ticket_id>/<new_status>', methods=["GET"])
def update_status(ticket_id, new_status):
    ticket_row = Ticket.query.get(ticket_id)
    ticket_row.status = new_status
    db.session.commit()
    return redirect("/dashboard")


@app.route("/update_record/<int:ticket_id>", methods=['GET'])
def update_record(ticket_id):
    ticket_row = Ticket.query.get(ticket_id)
    return render_template('update.html',ticket=ticket_row)


@app.route("/update_ticket_action", methods=["POST"])
def update_action():
    ticket_id = request.form['ticket_id']
    ticket_row = Ticket.query.get(ticket_id)
    ticket_row.title = request.form['title']
    ticket_row.description = request.form['description']
    ticket_row.status = request.form['status']
    db.session.commit()
    return redirect('/dashboard')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/tickets_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# User model (add to existing models)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='user')


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add relationship to User
    author = db.relationship('User', backref=db.backref('tickets', lazy=True))


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Identity loader
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(RoleNeed(current_user.role))


# Admin route
@app.route('/admin')
@admin_permission.require(http_exception=403)
@login_required
def admin_dashboard():
    all_tickets = Ticket.query.all()
    return render_template('admin_dashboard.html', tickets=all_tickets)


if __name__ == "__main__":
    app.run(debug=True)
