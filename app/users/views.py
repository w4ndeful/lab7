from . import bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta, datetime

@bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        return render_template("profile.html", username=username_value)
    flash("Invalid: Session.", "danger")
    return redirect(url_for("users.login"))

@bp.route('/set_color/<string:color>')
def set_color(color):
    resp = make_response(redirect(url_for('users.get_profile')))
    resp.set_cookie('color_scheme', color, max_age=3600*24*30) # місяць
    return resp


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["login"]
        password = request.form["password"]  

        if username == "Ivan" and password == "Ivan": 
            session["username"] = username
            flash("Успішний вхід!", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Невірний логін або пароль!", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html")

@bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('users.get_profile'))



@bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", name=name, age=age)

@bp.route("/admin")
def admin():
    to_url = url_for("user.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)


from flask import make_response

@bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if "username" in session:
        key = request.form.get('key')
        value = request.form.get('value')
        max_age = int(request.form.get('max_age', 3600))  # За замовчуванням 1 година

        if key and value:
            resp = make_response(redirect(url_for('users.get_profile')))
            resp.set_cookie(key, value, max_age=max_age)
            flash(f"Кукі '{key}' додано успішно!", "success")
            return resp
        else:
            flash("Помилка: Вкажіть ключ та значення кукі.", "danger")

    return redirect(url_for('users.get_profile'))



@bp.route('/delete_cookie_by_key', methods=['POST'])
def delete_cookie_by_key():
    if "username" in session:
        key = request.form.get('key')
        if key:
            resp = make_response(redirect(url_for('users.get_profile')))
            resp.set_cookie(key, '', expires=0) 
            flash(f"Кукі '{key}' видалено успішно!", "success")
            return resp
        else:
            flash("Помилка: Вкажіть ключ кукі для видалення.", "danger")
        
    return redirect(url_for('users.get_profile'))



@bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if "username" in session:
        resp = make_response(redirect(url_for('users.get_profile')))
        for key in request.cookies:
            resp.set_cookie(key, '', expires=0)
        flash("Всі кукі видалено успішно!", "success")
        return resp

    return redirect(url_for('users.get_profile'))