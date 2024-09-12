from flask import Flask, request, jsonify, redirect, render_template
from mongoengine import connect
from datetime import datetime
from models import CompactUrl
from flask_pydantic import validate
from schemas import UrlCreateSchema, UrlResponseSchema, UrlStatsResponseSchema


app = Flask(__name__)
app.config["DEBUG"] = True


def init_db(host="mongodb://127.0.0.1:27017/url_shortener", **kwargs):
    connect(host=host, **kwargs)


@app.route("/shorten", methods=["POST"])
@validate()
def create_url(body: UrlCreateSchema):
    new_url = CompactUrl(**body.dict())

    if CompactUrl.objects(short_code=new_url.short_code):
        return "Bad Request", 400

    new_url.save()
    return jsonify(UrlResponseSchema.from_orm(new_url).dict()), 201


@app.route("/shorten/<short_url>", methods=["GET"])
@validate()
def get_original_url(short_url):
    url = CompactUrl.objects(short_code=short_url).first()

    if not url:
        return "Not Found", 404

    url.access_count = url.access_count + 1
    url.save()
    return jsonify(UrlResponseSchema.from_orm(url).dict()), 200


@app.route("/shorten/<short_url>", methods=["PUT"])
@validate()
def update_url(short_url, body: UrlCreateSchema):
    url = CompactUrl.objects(short_code=short_url).first()

    if not url:
        return "not found", 404

    url.url = body.url
    url.updated_at = datetime.now()
    url.save()

    return jsonify(UrlResponseSchema.from_orm(url).dict()), 200


@app.route("/shorten/<short_url>", methods=["DELETE"])
@validate()
def delete_url(short_url):
    url = CompactUrl.objects(short_code=short_url).first()

    if not url:
        return "not found", 404

    url.delete()
    url.save()

    return "No Content", 204


@app.route("/shorten/<short_url>/stats", methods=["GET"])
def get_stats(short_url):
    url = CompactUrl.objects(short_code=short_url).first()
    if not url:
        return "Not Found", 404

    return jsonify(UrlStatsResponseSchema.from_orm(url).dict()), 200


@app.route("/<short_code>")
def redirect_to_url(short_code):
    url = CompactUrl.objects(short_code=short_code).first()
    if not url:
        return "Not Found", 404

    url.access_count += 1
    url.save()

    return redirect(url.url)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run()


# TODO: Add admin page to update, delete, list urls
# TODO: Add authentication for update, delete and all other admin operations
# TODO: Add swagger
# TODO: Make sure same url gets same short code
