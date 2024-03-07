from flask import Blueprint, render_template, request, flash, redirect
from auth import login_required
import os

images_bp = Blueprint('images_endpoints', __name__, template_folder='templates/blog')


@images_bp.route('/add_images', methods=['GET'])
@login_required
def upload_images_template():
    return render_template('upload_image.html')


@images_bp.route('/upload_images', methods=['GET', 'POST'])
@login_required
def upload_image():
    files = request.files.getlist('picture')

    for file in files:
        img_path = os.path.join(os.environ.get('IMG_POST'), file.filename)
        file.save(img_path)

    flash('Pomyślnie dodano zdjęcia!')

    return redirect('/admin')


@images_bp.route('/delete_images', methods=['GET'])
@login_required
def delete_images_template():
    return render_template('delete_image.html')

