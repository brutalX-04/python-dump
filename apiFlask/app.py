from flask import Flask, Blueprint, render_template
from extensions import mongo
from tiktok.routes import tiktok
from instagram.routes import instagram
from tools.count import get_count, update_count
from tools.download import download_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    mongo.init_app(app)

    app.register_blueprint(tiktok, url_prefix="/api/tiktok/")
    app.register_blueprint(instagram, url_prefix="/api/instagram/")
    app.register_blueprint(download_bp, url_prefix="/download/")

    return app


app = create_app()

@app.route("/")
def home():
    update_count()
    count = get_count()
    print(count)
    return render_template("home.html", count=count)




if __name__ == "__main__":
    app.run(debug=True)