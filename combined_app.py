from flask import Flask, render_template, redirect, url_for
from mental_health.app import create_mental_health_app
from legal_chatbot.app import create_legal_chatbot_app

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    mental_health = create_mental_health_app()
    legal_bot = create_legal_chatbot_app()

    app.register_blueprint(mental_health, url_prefix="/mental-health")
    app.register_blueprint(legal_bot, url_prefix="/legal-bot")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
