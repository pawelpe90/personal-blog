FROM python:3.11

WORKDIR /app

COPY ./blog .
RUN pip3 install -r requirements.txt

EXPOSE 80:5000

CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0"]
