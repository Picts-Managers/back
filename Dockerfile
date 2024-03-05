FROM python:3.11-alpine
WORKDIR /app

ENV TZ='Europe/Paris'

EXPOSE 3000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "gunicorn", "-c", "gunicorn_conf.py", "wsgi:app"]
