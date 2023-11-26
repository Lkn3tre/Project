import os, json , smtplib
from email.mime.text import MIMEText
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user,UserMixin
from .admin.routes import admin
from data.data import *

app = Flask(__name__)
app.register_blueprint(admin)

app.config["SECRET_KEY"] = '123'
app.config["E-Mail"] = "noureddinezf09@gmail.com"
app.config["GMAIL_APP_PASSWORD"] = os.environ.get("token")

Bootstrap(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
render = False
class User(UserMixin):
    def __init__(self, user_id, name ,email, password , admin):
        self.id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin

#This function for sending email when the purchase is made
def send_email(subject, body, to_email, from_email, app_password):
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, message.as_string())

@app.context_processor
def inject_now():
	""" sends datetime to templates as 'now' """
	return {'now': datetime.utcnow()}

@login_manager.user_loader
def load_user(user_id):
	user = get_user_by_id(user_id)
	try:
		return User(user[0],user[1],user[2],user[3],user[4])
	except Exception as ex:
		return str(ex) # Quand on le cree pour la premiere fois , user is None

@app.route("/")
def home():
	items = get_all_items()
	return render_template("home.html", items=items,render=True)

@app.route("/login", methods=['POST', 'GET'])
def login():
	if isinstance(current_user,str):
		pass
	elif current_user.is_authenticated:
		return redirect(url_for('home'))
	if request.method  == 'POST':
		email = request.form.get('mail')
		password = request.form.get('password')
		user = get_user_by_email(email)
		try:
			user = User(user[0],user[1],user[2],user[3],user[4])
			if check_password_hash(user.password, password):
				login_user(user)
				return redirect(url_for('login'))
			else:
				flash("Email and password incorrect!!", "error")
				return redirect(url_for('login'))
		except:
			flash("please check your credentials", "error")
			return redirect(url_for('login'))
	return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
	if isinstance(current_user,str):
		pass
	elif current_user.is_authenticated:
		return redirect(url_for('home'))
	if request.method  == 'POST':
		name = request.form.get('name')
		email = request.form.get('mail')
		password = request.form.get('password')
		user = get_user_by_email(email)
		if user:
			flash(f"User with email {user[2]} already exists!!<br> <a href={url_for('login')}>Login now!</a>", "error")
			return redirect(url_for('register'))

		new_user = register_user(name=name,
						email=email,
						password=generate_password_hash(
									password,
									method='pbkdf2:sha256',
									salt_length=8))
		flash('Thanks for registering! You may login now.', f'success')

		return redirect(url_for('login'))
	return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route("/add/<id>", methods=['POST'])
@login_required
def add_to_cart(id):
	if not current_user.is_authenticated:
		flash(f'You must login first!<br> <a href={url_for("login")}>Login now!</a>', 'error')
		return redirect(url_for('login'))

	item = get_item_by_id(id)
	if request.method == "POST":
		quantity = request.form["quantity"]
		add_to_cart_db(current_user.id, id, quantity)
		flash(f'''{item[1]} successfully added to the <a href=cart>cart</a>.<br> <a href={url_for("cart")}>view cart!</a>''','success')
		return redirect(url_for('home'))

@app.route("/cart")
@login_required
def cart():
	price=0
	price_ids = []
	quantity = []
	user_items = get_user_items(current_user.id)
	for cart in user_items:
		quantity.append(cart[3])
		price_id_dict = {
			"price": cart[4],
			"quantity": cart[3],
			}
		price_ids.append(price_id_dict)
		price += cart[3]*cart[2]
	return render_template('cart.html',  items = user_items , price=price, price_ids=price_ids, quantity=quantity)


@app.route("/remove/<id>/<quantity>")
@login_required
def remove(id, quantity):
	remove_from_cart_by_id(id)
	return redirect(url_for('cart'))

@app.route('/item/<int:id>')
def item(id):
	item = get_item_by_id(id)
	return render_template('item.html', item=item)


@app.route('/search')
def search():
	query = request.args['query']
	query = f"%{query}%"
	items = search_in_items(query)
	return render_template('home.html', items=items, search=True, query=query[1:][:-1])

@app.route('/payment_success')
def payment_success():
	return render_template('success.html')

@app.route('/payment_failure')
def payment_failure():
	return render_template('failure.html')

@app.route('/pay', methods=['POST','GET'])
def pay():
	ordered_items = get_all_cart_items(current_user.id)
	if request.method =='POST':
		for item in ordered_items:
			remove_from_cart_by_id(item[0])
			to_email = current_user.email
			subject = "Payment"
			Body = "Your payment was successfully made , hope you like our services"
			send_email(subject , Body, to_email,app.config["E-Mail"],app.config["GMAIL_APP_PASSWORD"])
		return redirect(url_for('payment_success'))
	return render_template('pay.html')
