from flask import Blueprint, render_template, request, get_flashed_messages
from utils.db_utils import get_all_tags, query_post
from auth import login_required

post_bp = Blueprint('posts_endpoints', __name__, template_folder='templates/blog')


@post_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def create_new_post():

    tags = get_all_tags()

    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('new_post.html', messages=messages, tags=tags)

    if request.method == 'POST':
        return render_template('new_post.html')


@post_bp.route('/update_post', methods=['GET', 'POST'])
@login_required
def update_post():

    tags = get_all_tags()
    post_id = request.args.get('id')
    post = query_post(post_id)

    tags_list = [tag.category for tag in post.tags]

    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('update_post.html', messages=messages, tags=tags, post=post, checked_tags=tags_list)

    if request.method == 'POST':
        return render_template('update_post.html')
