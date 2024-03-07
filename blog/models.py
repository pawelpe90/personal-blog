from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

association_table = Table(
    'posts_to_tags',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('id_post', Integer, ForeignKey('blog_posts.id')),
    Column('id_tags', Integer, ForeignKey('tags.id'))
)


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime(), default=datetime.now)
    update_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    views = Column(Integer)
    title = Column(String(50))
    content = Column(String(100))
    summary = Column(String(255))
    preview_img = Column(String(50))

    tags = relationship('Tags', secondary=association_table, back_populates='blog_posts')

    def __repr__(self):
        return f'(id:{self.id}, categories:{self.tags})'


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    category = Column(String(50))

    blog_posts = relationship('BlogPost', secondary=association_table, back_populates='tags')

    def __repr__(self):
        return f'{self.category}'

    def __str__(self):
        return f'{self.category}'


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(255))

    def __repr__(self):
        return f'("id":{self.id}, username:{self.username}, password:{self.password})'
