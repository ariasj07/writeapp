from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, Response, make_response
crud = Blueprint('crud', __name__)
from modules import SQLiteasy
from functools import wraps
from route import check_user

entries = {
    "created_by_user_name": {"type": "string", "notnull": True},
    "created_by_user_id": {"type": "string", "notnull": True},
    "title": {"type": "string", "notnull": True},
    "description": {"type": "string", "notnull": True},
    "content": {"type": "string", "notnull": True},
    "date": {"type": "string", "notnull": True},
    "post_id": {"type": "string", "notnull": True},
    "post_cover": {"type": "string", "notnull": True},
}

entries2 = {
    "user_email": {"type": "string", "notnull": True},
    "suscribed_to": {"type": "string", "notnull": True},
    "suscribed_from": {"type": "string", "notnull": True},
    "suscribed_date": {"type": "string", "notnull": True},
}

database = SQLiteasy("posts", entries)
database.create_database()

registers = SQLiteasy("registers", entries2)
registers.create_database()




#/change/add
@crud.route('/add')
@check_user # <- if there's no user on session this decorator send the user to register, its a blocker for non-registered users
def add():
    user = session.get("user")
    return render_template("./crud/index.html", user=user)

def get_user():
    return session.get('user', None)


def generate_id():
    import random
    a = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(random.sample(a, 10))

@crud.route("/send", methods=["POST"])
def send():
    from user.views import users_db
    user_id = session.get("user_id")
    user_info = users_db.fetch_database_by("user_id", user_id)
    title = request.form.get("post_title")
    description = request.form.get("post_description")
    content = request.form.get("post_content")
    cover = request.form.get("post_cover")
    if not title and description and content and cover:
        return render_template("./extra/error.html", message="Fill all the inputs")
    else:
        database.insert_database(created_by_user_name=user_info[0][3], created_by_user_id=user_id, title=title, description=description, content=content, date="25-01-2025", post_id=generate_id(), post_cover=cover)
        return redirect(url_for('crud.admin'))



@crud.route("/update/<post_id>", methods=["POST"])
def update(post_id):
    from user.views import users_db
    user_id = session.get("user_id")
    user_info = users_db.fetch_database_by("user_id", user_id)
    title = request.form.get("post_title")
    description = request.form.get("post_description")
    content = request.form.get("post_content")
    cover = request.form.get("post_cover")

    if not title and description and content and cover:
        return render_template("./extra/error.html", message="Fill all the inputs")
    else:
        database.update_database_by("title", "post_id", post_id, title)
        database.update_database_by("description", "post_id", post_id, description)
        database.update_database_by("content", "post_id", post_id, content)
        database.update_database_by("post_cover", "post_id", post_id, cover)

        return redirect(url_for("crud.admin"))

@crud.route('/suscribe<user>')
def suscribe(user):
    return user


@crud.route("/admin")
@check_user # <- imported from route.py. It checks whether the user has a session logged in or not. if so it will call the below function, if not it will call for the register template
def admin():
    from user.views import users_db
    user_id = session.get("user_id")
    user_info = database.fetch_database_by("created_by_user_id", user_id)
    user = users_db.fetch_database_by("user_id", user_id)
    if user_info:
        print("hay user")
        return render_template("./crud/admin.html", data=user_info, user=user_id)
    else:
        print("no user")
        return render_template("./crud/admin.html", user=user_id)

@crud.route("/dashboard")
@check_user # <- imported from route.py. It checks whether the user has a session logged in or not. if so it will call the below function, if not it will call for the register template
def dashboard():
    from user.views import users_db
    user_id = session.get("user_id")
    user_info = database.fetch_database_by("created_by_user_id", user_id)
    user = users_db.fetch_database_by("user_id", user_id)
    if user_info:
        return render_template("./crud/admin_content.html", data=user_info, user=user_id)
    else:
        return render_template("./crud/admin_content.html", user=user_id)
    
@crud.route("/create")
@check_user # <- imported from route.py. It checks whether the user has a session logged in or not. if so it will call the below function, if not it will call for the register template
def create(): # <- Loads the create page
    user_id = session.get("user_id")
    if request.headers.get("HX-Request"):
        return render_template("./crud/index.html")
    else:
        return redirect(url_for('crud.admin'))

@crud.route("/stats")
@check_user # <- imported from route.py. It checks whether the user has a session logged in or not. if so it will call the below function, if not it will call for the register template
def stats():
    print("stats")
    user_id = session.get("user_id")
    from user.views import users_db
    data = database.fetch_database_by("created_by_user_id", user_id)
    if data:
        posts = len(data)
        all_registers = registers.fetch_database_by("suscribed_to", user_id)
        print(".,.,.,.,.,.,.")
        all_registers.sort(key=lambda x: x[-1], reverse=True)
        print(all_registers)
        print(".,.,.,.,.,.,.")
        visits = users_db.fetch_database_by("user_id", user_id)[0][5]
        return render_template("./crud/stats.html", all_registers=all_registers, visits=visits, posts=posts)
    else:
        return render_template("./crud/stats.html")
@crud.route("/edit/<post_id>")
@check_user
def edit(post_id):
    post_created_by = database.fetch_database_by("post_id", post_id)
    
    if post_created_by:
        creator = post_created_by[0][2] # <- it'll return the creator id of the fetched post 
    else:
        raise ValueError("Post not found")
    if creator == session.get("user_id"):
        if request.headers.get("HX-Request"):
            return render_template("./crud/edit.html", data=post_created_by)
        else:
            print("******")
            return redirect(url_for('crud.admin'))
    else:
        return ValueError("You don't have access to this section")

@crud.route("/delete/<post_id>")
@check_user
def delete(post_id):
    print(f"DELETE {post_id}")
    post_created_by = database.fetch_database_by("post_id", post_id)
    
    if post_created_by:
        creator = post_created_by[0][2] # <- it'll return the creator id of the fetched post 
    else:
        raise ValueError("Post not found")
    if creator == session.get("user_id"): # <- if the creator of the post is the same as the user logged in
        database.delete_database_row_by("post_id", post_id)
        return redirect(url_for('crud.admin'))
    else:   
        return ValueError("You don't have access to this section")

@crud.route("/profile")
@check_user
def profile():
    user_id = session.get("user_id")
    if user_id:
        from user.views import users_db
        posts = database.fetch_database_by("created_by_user_id", user_id) # returns all posts + id and name
        user_info = users_db.fetch_database_by("user_id", user_id) # it'll return email, name, password, id, visits, in that order
        return render_template("./crud/profile.html", posts=posts, user_info=user_info)
    else:
        raise ValueError("Something went wrong. Please contact us: Error code: 03")
    


    
    
