from flask import Blueprint, request, redirect, flash
from utils.db_utils import get_session
from models import Tags, BlogPost
from auth import login_required
import os

database_bp = Blueprint('database_endpoints', __name__, template_folder='db_templates')


@database_bp.route('/insert_post_to_database', methods=['GET', 'POST'])
@login_required
def insert_post():

    # Handling blog file
    uploaded_file = request.files['source']
    uploaded_img = request.files['picture']

    post_path = os.path.join(os.environ.get('POST_PATH'), uploaded_file.filename)
    img_path = os.path.join(os.environ.get('IMG_PATH'), uploaded_img.filename)

    uploaded_file.save(post_path)
    uploaded_img.save(img_path)

    # Handling tags using checkboxes
    category_names = []

    for field_name, field_value in request.form.items():
        if field_name.startswith('tag_'):
            category_names.append(field_name[4:])

    # Handling tags using regular form (for new tags)
    new_tags = request.form.get('tags')

    new_tags_temp = []

    if len(new_tags) > 0:
        new_tags_temp = [i.capitalize() for i in new_tags.split()]

    category_names += new_tags_temp

    # Handling remaining forms
    title = request.form.get('title')
    source = uploaded_file.filename
    short = request.form.get('short')
    picture = img_path

    # Inserting new post
    session = get_session()

    # List to store the Tags instances associated with the blog post
    tags_list = []

    # Process each category name
    for category_name in category_names:
        # Check if a tag with the specified category already exists
        existing_tag = session.query(Tags).filter_by(category=category_name).first()

        # If it exists, use the existing tag; otherwise, create a new one
        if existing_tag:
            new_tag = existing_tag
        else:
            # Create a new Tag instance
            new_tag = Tags(category=category_name)

            # Add the new_tag to the session only if it's a new one
            session.add(new_tag)
            session.commit()

        # Add the tag to the list
        tags_list.append(new_tag)

    # Create a new BlogPost instance and assign the list of tags to its tags attribute
    new_post = BlogPost(views=0,
                        title=title,
                        content=source,
                        summary=short,
                        preview_img=picture,
                        tags=tags_list)

    session.add(new_post)
    session.commit()

    flash(f'Pomyślnie dodano nowy post: {title}')

    return redirect('/admin')


@database_bp.route('/update_post_in_database', methods=['GET', 'POST'])
@login_required
def update_post():

    # Handling blog file
    uploaded_file = request.files['source']
    uploaded_img = request.files['picture']

    post_path = os.path.join(os.environ.get('POST_PATH'), uploaded_file.filename)
    img_path = os.path.join(os.environ.get('IMG_PATH'), uploaded_img.filename)

    if uploaded_file:
        uploaded_file.save(post_path)

    if uploaded_img:
        uploaded_img.save(img_path)

    # Handling tags using checkboxes
    category_names = []

    for field_name, field_value in request.form.items():
        if field_name.startswith('tag_'):
            category_names.append(field_name[4:])

    # Handling tags using regular form (for new tags)
    new_tags = request.form.get('tags')

    new_tags_temp = []

    if len(new_tags) > 0:
        new_tags_temp = [i.capitalize() for i in new_tags.split()]

    category_names += new_tags_temp

    # Handling remaining forms
    title = request.form.get('title')
    source = uploaded_file.filename
    short = request.form.get('short')
    picture = img_path

    # Updating existing post
    session = get_session()
    post_id = request.args.get('id')
    existing_post = session.query(BlogPost).get(post_id)

    existing_post.title = title
    existing_post.summary = short

    if uploaded_file:
        existing_post.content = source

    if uploaded_img:
        existing_post.preview_img = picture

    # Update tags associated with the post
    existing_post.tags.clear()

    # List to store the Tags instances associated with the blog post
    tags_list = []

    # Process each category name
    for category_name in category_names:
        # Check if a tag with the specified category already exists
        existing_tag = session.query(Tags).filter_by(category=category_name).first()

        # If it exists, use the existing tag; otherwise, create a new one
        if existing_tag:
            new_tag = existing_tag
        else:
            # Create a new Tag instance
            new_tag = Tags(category=category_name)

            # Add the new_tag to the session only if it's a new one
            session.add(new_tag)
            session.commit()

        # Add the tag to the list
        tags_list.append(new_tag)

    existing_post.tags = tags_list
    session.commit()

    flash(f'Pomyślnie aktualizowano post: {title}')

    return redirect('/admin')


@database_bp.route('/delete_post_from_database', methods=['GET', 'POST'])
@login_required
def delete_post():
    session = get_session()

    post_id = request.args.get('id')
    post_to_delete = session.query(BlogPost).get(post_id)
    post_title = post_to_delete.title

    session.delete(post_to_delete)
    session.commit()

    flash(f'Pomyślnie usunięto post: {post_title}')

    return redirect('/admin')
