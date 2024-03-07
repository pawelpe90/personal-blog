import os
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from models import BlogPost, Tags, Base


def get_session(echo=False):
    host = os.environ.get('DB_HOST')
    user = os.environ.get('DB_USER')
    database = os.environ.get('DB_DATABASE')
    password = os.environ.get('DB_PASSWORD')
    port = os.environ.get('DB_PORT')

    if not all((host, user, database, password)):
        raise ValueError('Database environment variables not set')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}', echo=echo)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def get_all_items() -> []:
    session = get_session()
    result = session.query(BlogPost)\
        .order_by(BlogPost.create_date.desc())\
        .options(orm.joinedload(BlogPost.tags))\
        .all()

    return result


def get_all_tags() -> []:
    session = get_session()
    result = session.query(Tags.category).distinct().all()

    return result


def update_post_counter(post_id: int) -> None:
    session = get_session()

    blog_meta = session.query(BlogPost).get(post_id)

    blog_meta.views += 1
    session.commit()


def filter_posts(tag: str) -> []:
    session = get_session()

    filtered_posts = session.query(BlogPost)\
        .filter(BlogPost.tags.any(Tags.category == tag)) \
        .options(orm.joinedload(BlogPost.tags))\
        .all()

    return filtered_posts


def delete_post(post_id: int) -> None:
    session = get_session()

    post_to_delete = session.query(BlogPost).get(post_id)

    session.delete(post_to_delete)
    session.commit()


def query_post(post_id: int) -> []:
    session = get_session()

    post_to_update = session.query(BlogPost).get(post_id)

    return post_to_update


def query_tag(tag_name: str) -> []:
    session = get_session()

    tag = session.query(Tags).get(tag_name)

    return tag


def add_item():
    session = get_session()

    # List of category names for the blog post
    category_names = ['Python', 'DIY']

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
                        title='Czwarty post testowy',
                        content='czwarty_test.html',
                        summary='Krótki opis tego co w czwartym poście. Test dla Basi.',
                        preview_img='static/blog_covers/cover4.jpg',
                        tags=tags_list)

    session.add(new_post)
    session.commit()



# add_item()
# items = get_all_items()
# for item in items:
#     for tag in item.tags:
#         print(tag.category)
# print(items[0].title)
# for i in range(30,34,1):
#     delete_post(i)
# delete_post(41)
# tags = get_all_tags()
# print(tags)
# for tag in tags:
#     print(tag.category)
# print(('DUpa',))

