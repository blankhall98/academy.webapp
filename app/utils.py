from flask import current_app
import os
from werkzeug.utils import secure_filename

def save_file(file, subfolder):
    """
    Save an uploaded file to a specific subfolder under 'static/uploads'.
    """
    # Base folder for static uploads
    base_folder = os.path.join(current_app.root_path, "static", "uploads")
    
    # Ensure the subfolder exists
    folder_path = os.path.join(base_folder, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the file securely
    filename = secure_filename(file.filename)
    filepath = os.path.join(folder_path, filename)
    file.save(filepath)

    # Return the relative path for use in templates (e.g., 'uploads/images/filename.jpg')
    return f"uploads/{subfolder}/{filename}"