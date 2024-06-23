from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# ========== LOGIN / REGISTER PAGE - VIEW ============


@app.route("/")
def index():
    return render_template("index.html")


# REGISTER - method - ACTION
@app.route("/users/register", methods=["POST"])
def user_register():
    # print(request.form)
    if not User.validate(request.form):
        return redirect("/")
    # 1 . hash the password
    pw_hashed = bcrypt.generate_password_hash(request.form["password"])
    # 2 . get the data dict ready with the new hashe pw to create a User
    # data = {
    #     "first_name": request.form["first_name"],
    #     "last_name": request.form["last_name"],
    #     "email": request.form["email"],
    #     "confirm": request.form["confirm_password"],
    #     "password": pw_hashed,
    # }
    data = {**request.form, "password": pw_hashed}
    # save user in DB
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/dash")


# Login - method - ACTION
@app.route("/users/login", methods=["POST"])
def user_login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    # if email not found
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect("/")
    # now check the password
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid credentials", "log")
        return redirect("/")

    # * if all is good
    print(f"===> id = {user_in_db.id}")
    session["user_id"] = user_in_db.id
    return redirect("/dash")





# ! ------- LOGOUT -------- action
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dash")
def dash():
    # ! Route Guard
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggedin_user = User.get_user_by_id(data)
    session["user_email"] = "a@a.com"
    return render_template("dash.html", loggedin_user=loggedin_user)