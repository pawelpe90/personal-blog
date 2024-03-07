CREATE TABLE posts_to_tags (
    id          SERIAL PRIMARY KEY,
    id_post     INT,
    id_tags     INT,
    CONSTRAINT fk_blog_posts FOREIGN KEY(id_post) REFERENCES blog_posts(id),
    CONSTRAINT fk_tags FOREIGN KEY(id_tags) REFERENCES tags(id)
);
