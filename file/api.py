"""
File Server port 2000
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
from route import karaokeList_route
from route import radioList_route
from route import ssbuList_route
from route import voiceList_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
register blueprint
"""
app.register_blueprint(karaokeList_route.app)
app.register_blueprint(radioList_route.app)
app.register_blueprint(ssbuList_route.app)
app.register_blueprint(voiceList_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=2000)