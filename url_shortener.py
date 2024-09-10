from flask import Flask, request, jsonify, redirect, render_template
from mongoengine import (
    Document,
    StringField,
    IntField,
    SequenceField,
    DateTimeField,
    connect,
)
import shortuuid
from datetime import datetime
import validators

SHORT_CODE_LEN = 6  # euqals to 22 million URLs


def _get_uuid():
    return shortuuid.ShortUUID().random(length=SHORT_CODE_LEN)


app = Flask(__name__)
app.config["DEBUG"] = True


def init_db(host="mongodb://127.0.0.1:27017/url_shortener", **kwargs):
    connect(host=host, **kwargs)


class Url(Document):
    id = SequenceField(primary_key=True)
    url = StringField(required=True)
    short_code = StringField(
        required=True, max_length=SHORT_CODE_LEN, min_length=SHORT_CODE_LEN, unique=True
    )
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
    access_count = IntField(required=True, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "short_code": self.short_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@app.route("/shorten", methods=["POST"])
def create_url():
    original_url = request.json["url"]
    if not validators.url(original_url):
        return "Bad Request", 400

    create_time = datetime.now()
    new_url = Url(
        url=original_url,
        short_code=_get_uuid(),
        created_at=create_time,
        updated_at=create_time,
    )

    if Url.objects(short_code=new_url.short_code):
        return "Bad Request", 400

    new_url.save()
    return jsonify(new_url.to_dict()), 201


@app.route("/shorten/<short_url>", methods=["GET"])
def get_original_url(short_url):
    urls = Url.objects(short_code=short_url)
    if not urls:
        return "Not Found", 404

    url = urls[0]
    url.access_count = url.access_count + 1
    url.save()
    return jsonify(url.to_dict()), 200


@app.route("/shorten/<short_url>", methods=["PUT"])
def update_url(short_url):
    urls = Url.objects(short_code=short_url)
    if not urls:
        return "not found", 404

    new_url = request.json["url"]
    if not validators.url(new_url):
        return "Bad Request", 400

    url = urls[0]
    url.url = new_url
    url.updated_at = datetime.now()
    url.save()

    return jsonify(url.to_dict()), 200


@app.route("/shorten/<short_url>", methods=["DELETE"])
def delete_url(short_url):
    urls = Url.objects(short_code=short_url)

    if not urls:
        return "not found", 404

    url = urls[0]
    url.delete()
    url.save()

    return "No Content", 204


@app.route("/shorten/<short_url>/stats", methods=["GET"])
def get_stats(short_url):
    urls = Url.objects(short_code=short_url)
    if not urls:
        return "Not Found", 404

    url = urls[0]
    url_dict = url.to_dict()
    url_dict["access_count"] = url.access_count
    return jsonify(url_dict), 200


@app.route("/<short_code>")
def redirect_to_url(short_code):
    urls = Url.objects(short_code=short_code)
    if not urls:
        return "Not Found", 404

    url = urls[0]
    url.access_count += 1
    url.save()

    return redirect(url.url)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run()
