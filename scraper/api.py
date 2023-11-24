"""
Scraper Server port 3000
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
from route import twitter_route
from route import holosong_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
register blueprint
"""
app.register_blueprint(twitter_route.app)
app.register_blueprint(holosong_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=3000)