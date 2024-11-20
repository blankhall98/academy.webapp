from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    """Create an initial admin user"""
    app = create_app()
    
    with app.app_context():
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            print("Error: This email is already registered!")
            return

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create the new admin user
        new_admin = User(username=username, email=email, password=hashed_password, is_admin=True)

        # Save the user to the database
        db.session.add(new_admin)
        db.session.commit()

        print(f"Admin user '{username}' created successfully!")

if __name__ == "__main__":
    create_admin()