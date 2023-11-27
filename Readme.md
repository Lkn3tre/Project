# Réalisé par 

`Noureddine Azfar
Zakaria toubali`

# Encadré par 
`Mr.Mahmoud EL HAMLAOUI`


## Description

Ceci est une description d'une plateforme de commerce en ligne développée avec Flask, un framework web en Python. Le projet intègre l'authentification des utilisateurs, un système de panier d'achats et un traitement sécurisé des paiements. L'application suit une structure modulaire avec des fichiers distincts pour les fonctionnalités utilisateur et administrateur. SQLite3 est utilisé pour un stockage et une récupération efficaces des données.

## Fonctionnalités Clés
Authentification Utilisateur : Authentification sécurisée des utilisateurs alimentée par Flask-Login.

Panier d'Achats : Les utilisateurs peuvent ajouter des articles à leur panier et procéder au paiement.

Gestion des Administrateurs : Un fichier supplémentaire gère les fonctionnalités administratives pour l'administration du site.

Notifications par E-mail : Les utilisateurs reçoivent des e-mails de lors d'une achat réussite.

## Stack Technologique :

Framework Backend : Flask

Base de Données : SQLite3

Gestion des E-mails : smtplib

Sécurité des Mots de Passe : Werkzeug

## Sommaire

1. [Modèle Utilisateur](#modèle-utilisateur)
2. [Fonction d'Envoi d'E-mails](#fonction-denvoi-de-mails)
3. [Routes](#routes)
    - [Page d'Accueil](#page-daccueil)
    - [Page de Connexion](#page-de-connexion)
    - [Page d'Inscription](#page-dinscription)
    - [Déconnexion](#déconnexion)
    - [Ajout au Panier](#ajout-au-panier)
    - [Vue du Panier](#vue-du-panier)
    - [Suppression du Panier](#suppression-du-panier)
    - [Détails d'un Article](#détails-dun-article)
    - [Recherche](#recherche)
    - [Création d'une Session de Paiement](#création-dune-session-de-paiement)
4. [Utilisation de SQLite3](#utilisation-de-sqlite3)
3. [Admin](#admin)

## Détails
### Modèle Utilisateur
Le modèle permet à Flask-Login de gérer les sessions utilisateur en stockant et récupérant les informations nécessaires à partir de l'objet `User` . Avec SQlite3 , Il est nécessaire d'inclure la création d'un objet de la classe User dans un block `try-except` .  Ceci car SQlite3 peut retourner `Nonetype` ce qui va lancer une exception dans le cas de notre code.
Par Exemple dans login on a mis:

```python
try:
	user = User(user[0],user[1],user[2],user[3],user[4])
	...
except :
	flash("please check your credentials", "error")
	...
```

Dans le cas où la fonction `get_user_by_email` retourne `None` ce qui signifie il n'y a aucun user avec l'email spécifié, the sentence `user[0]` va générer une exception .

### Fonction d'Envoi d'E-mails
La fonction d'envoi d'e-mail dans le code  utilise la bibliothèque Python `smtplib` pour envoyer des e-mails à l'aide du protocole SMTP . Pour cela elle est besoin de l'email qui sera simplement l'email de l'application Flask (dans ce cas c'est mon e-mail) et un `app_password` pour l'authentification qui sera stocké dans une variable d'environnement appelé `token` . Quand l'achat est réussite un email est envoyé a l'utilisateur comme ce qui suit montre:

```python
to_email = current_user.email
subject = "Payment"
Body = "Your payment was successfully made , hope you like our services"
send_email(subject , Body, to_email,app.config["E-Mail"],app.config["GMAIL_APP_PASSWORD"])
```

### Routes
#### Page d'Accueil
La page d'accueil va simplement recevoir all itmes du database et les afficher .

```python
@app.route("/")
def home():
	items = get_all_items()
	return render_template("home.html", items=items,render=True)
```

#### Page de Connexion
La page de connexion offre aux utilisateurs une interface sécurisée pour accéder à leur compte personnel sur la plateforme . Elle est constitué principalement d'un formulaire creé en `html` ce qui fournit une meilleur fléxibilité , les données reçu sont verifié en backend . Dans le code il y'a un vérification si `current_user` est une instance de la classe `str` , ce cas est possible car `login_manager` retourne dans notre cas `str` si la session n'est ouverte par aucun user

```python
@login_manager.user_loader
def load_user(user_id):
	user = get_user_by_id(user_id)
	try:
		return User(user[0],user[1],user[2],user[3],user[4])
	except Exception as ex:
		return str(ex) 
...
@app.route("/login", methods=['POST', 'GET'])
def login():
	if isinstance(current_user,str):
		pass
	...
```

#### Page d'inscription
La page d'inscription est tellement simple , il reçoit les informations par un formulaire et tester s'il y a déjà un utilisateur avec l'email reçu , s'il y en a un message d'erreur notifie l'utilisateur , s'il n y en a pas les informations sont ajoutées à la base de données avec un id qui s'incrémente à chaque fois un utilisateur est ajouté à la base de données .

```python
@app.route("/register", methods=['POST', 'GET'])
def register():
	...
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
	...
```

#### Déconnexion
La fonction `logout` permer la déconnexion de l'utilisateur en utilisant la fonction `logout_user` du `flask_login`

#### Ajout au Panier
la fonction add_to_cart permet d'ajouter au tableau `cart` dans la base de données des `items` que l'utilisateur veut acheter .Il nécesite l'authentification , sinon il envoie un message d'erreur . Si l'utilisateur est authentifié il utilse la fonction `add_to_cart_db` , envoie un message de succés et redirige l'utilisatuer vers `home` .

#### Vue de panier
La vue du panier offre aux utilisateurs une perspective claire et organisée de leurs articles sélectionnés. Cette page constitue le point central pour examiner les produits choisis . Elle calcule le prix total et donne à l'utilisateur l'opportunite d'ajouter de nouveau produits , supprimer ou payer . Elle fait appel principalement à la fonction `get_user_items` qui liste le contenu de la carte pour un utilisateur choisi.
```python
user_items = get_user_items(current_user.id)
```

#### Suppression du panier
La Suppression du panier permet de supprimer un produit de la carte.

#### Détails d'un Article
La route `/item/<int:id>` permet de donnez tous les détails d'un produit de la base de données ainsi de l'ajouter à la carte .

#### Recherche
Permet de rechercher un élément de la base donne suivant le nom de l'article , il fait appel à la fonction `search_in_items` qui implémente une simple recherche dans la base de données .

```python
@app.route('/search')
def search():
	query = request.args['query']
	query = f"%{query}%"
	items = search_in_items(query)
	return render_template('home.html', items=items, search=True, query=query[1:][:-1])
```

#### Création d'une Session de Paiement
Celle-ci creé un formulaire de paiement , supprime les articles achetées de la carte de l'utilisateur et envoie un e-mail à l'utilisateur norifiant le que son paiement a été bien éffectué .
```python
remove_from_cart_by_id(item[0])
to_email = current_user.email
subject = "Payment"
Body = "Your payment was successfully made , hope you like our services"
send_email(subject , Body, to_email,app.config["E-Mail"],app.config["GMAIL_APP_PASSWORD"])
```

### Utilisation de SQlite3 
Le fichier de la base de données se situe au dossier `data` et contient les fonctions nécessaires comme `create_users_table` , `search_in_items` , `update_item_by_id` et `remove_from_cart_by_id` ... pour créer , rechercher , modifier et supprimer .

### Admin
Le dossier `admin` est un dossier spéciales qui permet à l'admin de modifier les articles dans la base de données , il offre des fonctionnalitées d'ajout , de modification et de suppression des éléments. Les éléments sont crées et modifiés à l'aide d'un formulaire en `html` et supprimées par un click .
