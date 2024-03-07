docker build -t postgres_blog_image:3 .
docker run -p 5434:5432 --name blog_db postgres_blog_image:3