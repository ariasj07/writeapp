from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from modules import SQLiteasy
from crud.views import generate_id

user = Blueprint('user', __name__)

@user.route('/post/<post_id>')
def post(post_id):
    from crud.views import database
    from .test import convert
    from user.views import users_db
    data = database.fetch_database_by("post_id", post_id)
    user_id = data[0][2]
    user_info = users_db.fetch_database_by("user_id", user_id)
    content = convert(data[0][5])
    """ logica para añadir visit """
    from crud.views import database
    created_by = database.fetch_database_by("post_id", post_id)[0][2]
    current_visits = users_db.fetch_database_by("user_id", created_by)[0][5] + 1
    users_db.update_database_by("user_visits", "user_id", created_by, current_visits)
    return render_template("./user/post.html", data=data, content=content, user_info=user_info)

@user.route("/profile/<user_id>")
def profile(user_id):
    from user.views import users_db
    from crud.views import database
    user_info = users_db.fetch_database_by("user_id", user_id)
    return render_template("./user/profile.html", data=database.fetch_database_by("created_by_user_id", user_id), user_info=user_info)
    
    

@user.route("/suscribe/<user>")
def suscribe(user):
    from crud.views import database
    user_info = database.fetch_database_by("created_by", user)
    return render_template("./user/suscribe.html", data=user_info)

@user.route("/suscribed", methods=["POST"])
def suscribed():
    from crud.views import registers
    user_email = request.form.get("user_email")
    suscribed_to = request.form.get("suscribed_to")
    suscribed_from = request.form.get("suscribed_from")
    is_already_suscribed = registers.fetch_database_by_and("user_email", user_email, "suscribed_to", suscribed_to)
    print(".............")
    print(user_email)
    print(suscribed_to)
    print(suscribed_from)
    print(".............")
    if not is_already_suscribed:
        if user_email and suscribed_to:
            from datetime import datetime
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d %H:%M:%S')
            registers.insert_database(user_email=user_email, suscribed_to=suscribed_to, suscribed_from=suscribed_from, suscribed_date=now_str)
            return render_template("./extra/input.html", valid=True, message="You've suscribed!", value=user_email)
        else:
            raise ValueError("Something went wrong with the suscribe")
    else:
        return render_template("./extra/input.html", valid=False, message="You're already registered with this email", value=user_email)
    
user_entries = {
    "user_email": {"type": "string", "notnull": True},
    "user_name": {"type": "string", "notnull": True},
    "user_password": {"type": "string", "notnull": True},
    "user_id": {"type": "string", "notnull": True},
    "user_visits": {"type": "integer", "notnull": True},
    
}


users_db = SQLiteasy("users", user_entries)
users_db.create_database()

@user.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_id = request.form.get("user_id")
        user_email = request.form.get("user_email")
        is_already_registered = users_db.fetch_database_by_or("user_email", user_email, "user_id", user_id)
        print("******************")
        print(user_name)
        print(user_id)
        print(user_email)
        print(is_already_registered)
        print("******************")
        if not is_already_registered:
            user_password = request.form.get("user_password")
            if len(user_email.split("@")[0]) < 5:
                return render_template('register.html', error="Use a real email address")
            users_db.insert_database(user_email=user_email, user_name=user_name, user_password=user_password, user_id=user_id, user_visits=0)
            session["user_id"] = user_id
            return redirect(url_for('crud.admin'))
        else:
            print("error")
            return render_template("register.html", error="This user is already register. Please login")
    else:
        return render_template("register.html")
    
@user.route("/login")
def login():
    return render_template('./login.html')

@user.route("/logged", methods=["POST"])
def logged():
    email_or_username = request.form.get("email_or_username")
    password = request.form.get("password")
    print("_______________-")
    print(email_or_username)
    print(password)
    print("_______________-")
    user = users_db.fetch_database_by("user_id", email_or_username)
    if user:
        current_pass = user[0][3]
        if current_pass == password:
            session["user_id"] = email_or_username
            return redirect(url_for("crud.admin"))
        else:
            return render_template("login.html", error="The password is not correct")
    else:
        return render_template("login.html", error="This account does not exists, create one please")
