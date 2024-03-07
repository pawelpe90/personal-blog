CREATE TABLE blog_posts (
    id          SERIAL PRIMARY KEY,
    create_date TEXT NOT NULL,
    update_date TEXT,
    views       INT DEFAULT 0,
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    summary     TEXT NOT NULL,
    preview_img TEXT NOT NULL
);