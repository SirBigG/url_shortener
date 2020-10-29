import os
import logging
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, Response

from peewee import OperationalError

from models import database, Url

from decoders import Base62


app = Flask(__name__)
app.config["SERVER_NAME"] = os.getenv("SERVER_NAME")


@app.before_request
def before_request():
    # Catch Connection already opened error
    try:
        database.connect()
    except OperationalError as e:
        logging.error(e)


@app.after_request
def after_request(response):
    database.close()
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if urlparse(original_url).scheme == '':
            original_url = f'http://{original_url}'
        url = Url.select().where(Url.url == original_url).first()
        if url:
            return render_template("index.html",
                                   short_url=f"{request.scheme}://{app.config['SERVER_NAME']}/{Base62.encode(url.id)}",
                                   views=url.views)
        with database.atomic():
            url = Url.create(url=original_url)
        return render_template("index.html",
                               short_url=f"{request.scheme}://{app.config['SERVER_NAME']}/{Base62.encode(url.id)}")
    return render_template('index.html')


@app.route('/<short_url>')
def short_url_redirect(short_url):
    url_id = Base62.decode(short_url)
    url = Url.select().where(Url.id == url_id).first()
    if url:
        url.views += 1
        url.save()
        return redirect(url.url)
    return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)
