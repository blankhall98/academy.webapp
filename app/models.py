from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Campo para distinguir administradores
    courses = db.relationship("UserCourse", backref="user", lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    promo_image = db.Column(db.String(200), nullable=True)  # URL to the promotional image
    syllabus = db.Column(db.String(200), nullable=True)  # URL to the syllabus PDF
    start_date = db.Column(db.Date, nullable=True)  # Fecha de inicio
    class_days = db.Column(db.String(200), nullable=True)  # Días de clase
    class_time = db.Column(db.String(50), nullable=True)  # Horario

class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)