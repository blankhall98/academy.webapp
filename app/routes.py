from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Course, UserCourse
from .extensions import db

bp = Blueprint('main', __name__)

# Ruta principal
@bp.route("/")
def index():
    return render_template("index.html")

# Registro de usuarios
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #buscar en el form la información
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]


        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(password, method="sha256")

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")

# Inicio de sesión
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")

# Cerrar sesión
@bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("main.index"))

# Cursos disponibles
@bp.route("/courses")
def courses():
    all_courses = Course.query.all()
    return render_template("cursos.html", courses=all_courses)

# Compra de cursos
@bp.route("/courses/<int:course_id>/buy")
def purchase_course(course_id):
    if "user_id" not in session:
        flash("Inicia sesión para comprar un curso.", "danger")
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    if UserCourse.query.filter_by(user_id=user_id, course_id=course_id).first():
        flash("Ya adquiriste este curso.", "info")
        return redirect(url_for("main.courses"))

    new_purchase = UserCourse(user_id=user_id, course_id=course_id)
    db.session.add(new_purchase)
    db.session.commit()

    flash("Curso adquirido exitosamente.", "success")
    return redirect(url_for("main.user_courses"))

# Historial de cursos adquiridos
@bp.route("/my-courses")
def user_courses():
    if "user_id" not in session:
        flash("Inicia sesión para ver tus cursos.", "danger")
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    user_courses = UserCourse.query.filter_by(user_id=user_id).all()
    return render_template("historial.html", courses=user_courses)
