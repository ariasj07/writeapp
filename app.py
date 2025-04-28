from flask import Flask, render_template, request, redirect, url_for, session
from crud.views import crud
from user.views import user

app = Flask(__name__)
app.secret_key = "123"
app.register_blueprint(crud, url_prefix='/change')
app.register_blueprint(user, url_prefix='/user')



def check_user(original):
    def check():
        user = session.get("user")
        if user not in session:
            return render_template('main.html')
        else:
            original()
    
def get_user():
    return session.get('user', None)

def get_data_by_user(user):
    from crud.views import database    
    return database.fetch_database_by("created_by", get_user())

@app.route('/')
def index():
    return render_template('index.html')
@app.errorhandler(Exception)
def error(e):
    return render_template("./extra/bad.html", error=e)

if __name__ == '__main__':
    app.run(debug=True)