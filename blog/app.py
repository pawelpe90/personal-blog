from flask import Flask, render_template, request, get_flashed_messages
from auth import login_bp
from posts import post_bp
from db import database_bp
from images import images_bp
from utils.db_utils import get_all_items, update_post_counter, get_all_tags, filter_posts
from auth import login_required

app = Flask(__name__)
app.config.from_prefixed_env()

app.register_blueprint(login_bp)
app.register_blueprint(post_bp)
app.register_blueprint(database_bp)
app.register_blueprint(images_bp)


@app.route('/')
def index():
    messages = get_flashed_messages()

    if request.args.get('tag') is None:
        posts_meta = get_all_items()
        all_tags = get_all_tags()

    else:
        tag = request.args.get('tag')
        posts_meta = filter_posts(tag)
        all_tags = get_all_tags()

        if len(posts_meta) == 0:
            posts_meta = None

    context = {'posts_meta': posts_meta, 'tags': all_tags, 'messages': messages}

    return render_template('blog/index.html', **context)


@app.route('/admin')
@login_required
def admin():
    posts_meta = get_all_items()
    messages = get_flashed_messages()

    context = {"posts_meta": posts_meta, "messages": messages}

    return render_template('blog/admin.html', **context)


@app.route('/blog')
def load_post():
    file = request.args.get('file')
    post_id = request.args.get('id')
    all_tags = get_all_tags()

    update_post_counter(post_id)

    context = {"tags": all_tags}

    return render_template('posts/' + file, **context)


if __name__ == '__main__':
    app.run(debug=True)
