from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.rent import Rent
from flask_bcrypt import Bcrypt #pour crypter le mot de passe de l'utilisateur et sauvegarder les caractéristiques du mot de passe
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/') 
def index():
    return render_template("index.html")

@app.route('/users/create',methods=['POST'])
def create_user():
    # print(request.form)
    if(User.validate(request.form)):        #request.form: les données envoyées par l'utilisateur dans le formulaire
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            **request.form,'password':pw_hash   #**request.form: les 2* vont transformées tous les dictionnaires en instances
        }
        user_id = User.create_user(data)
        session['user_id'] = user_id   #on met l'id de l'utilisateur dans la session pour vérifier si l'utilisateur est connécté ou nn
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:  #si l'id de l'utilisateur n'existe pas dans la session, le serveur va le conduire vers la page index.html pour qu'il puisse connecter et entrer au dashboard (enregistrer l'email et le mot de passe)  
        return redirect('/')
    user = User.get_by_id({'id':session['user_id']})
    pokemons=Pokemon.get_pokemon_by_user({'user_id':session['user_id']}) 
    return render_template("dashboard.html", user = user,pokemons=pokemons)  #user = user: on est en train d'envoyer le nom de l'utilisateur puisqu'on est en train d'afficher le nom de l'utilisateur

@app.route('/users/login', methods=['POST'])
def login():
    user_from_db = User.get_by_email({'email':request.form['email']})
    if(user_from_db):
        # check password
        if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):     #user_from_db.password, request.form['password']:dans cette phase, on va comparer le mot de passe enregistré dans la session avec le mot de passe que l'utlisateur a mis
        # if we get False after checking the password
            flash("Invalid Password")
            return redirect('/')
        session['user_id'] = user_from_db.id
        return redirect('/dashboard')
    flash("Invalid Email")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')