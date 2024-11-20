from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Course, UserCourse
from .extensions import db
from functools import wraps
from flask import abort
from .utils import save_file
from datetime import datetime

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

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

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
            session["is_admin"] = user.is_admin  # Save admin status in session
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
    user_courses_ids = UserCourse.query.filter_by(user_id=user_id).all()
    user_courses = Course.query.filter(Course.id.in_([uc.course_id for uc in user_courses_ids])).all()
    return render_template("historial.html", courses=user_courses)

#################################################################
# ADMIN

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or not session.get("is_admin"):
            abort(403)  # Prohibido si no es administrador
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/admin/courses")
@admin_required
def admin_courses():
    courses = Course.query.all()
    return render_template("admin_courses.html", courses=courses)

@bp.route("/admin/courses/add", methods=["GET", "POST"])
@admin_required
def add_course():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        class_days = ", ".join(request.form.getlist("class_days"))  # Combine days into a string
        class_time = request.form["class_time"]

        # Handle optional files
        promo_image = None
        syllabus = None

        if "promo_image" in request.files and request.files["promo_image"].filename:
            promo_image = save_file(request.files["promo_image"], "images")

        if "syllabus" in request.files and request.files["syllabus"].filename:
            syllabus = save_file(request.files["syllabus"], "pdfs")

        new_course = Course(name=name, description=description, price=price,
                             promo_image=promo_image, syllabus=syllabus,start_date=start_date,
                             class_days=class_days, class_time=class_time)
        db.session.add(new_course)
        db.session.commit()
        flash("Curso agregado exitosamente.", "success")
        return redirect(url_for("main.admin_courses"))

    return render_template("add_course.html")

@bp.route("/admin/courses/edit/<int:course_id>", methods=["GET", "POST"])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        course.name = request.form["name"]
        course.description = request.form["description"]
        course.price = request.form["price"]

        course.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        course.class_days = ", ".join(request.form.getlist("class_days"))  # Combine days into a string
        course.class_time = request.form["class_time"]

        if "promo_image" in request.files and request.files["promo_image"].filename:
            course.promo_image = save_file(request.files["promo_image"], "images")

        if "syllabus" in request.files and request.files["syllabus"].filename:
            course.syllabus = save_file(request.files["syllabus"], "pdfs")

        db.session.commit()
        flash("Curso actualizado exitosamente.", "success")
        return redirect(url_for("main.admin_courses"))

    return render_template("edit_course.html", course=course)

@bp.route("/admin/courses/delete/<int:course_id>", methods=["POST"])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Curso eliminado exitosamente.", "success")
    return redirect(url_for("main.admin_courses"))

@bp.route("/admin/create-admin", methods=["GET", "POST"])
@admin_required
def create_admin():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Verifica si el correo ya está registrado
        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("main.create_admin"))

        # Crear el nuevo administrador
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_admin = User(username=username, email=email, password=hashed_password, is_admin=True)

        # Guardar en la base de datos
        db.session.add(new_admin)
        db.session.commit()

        flash(f"Administrador '{username}' creado exitosamente.", "success")
        return redirect(url_for("main.admin_courses"))

    return render_template("create_admin.html")

