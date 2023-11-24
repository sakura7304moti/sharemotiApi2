"""
Flask Server port 1000
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
from route import wordList2_route
from route import nameList_route
from route import yakiList_route
from route import schoolList_route
from route import mannerList_route
from route import haikuList_route
from route import imageList_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
register blueprint
"""
app.register_blueprint(wordList2_route.app)
app.register_blueprint(nameList_route.app)
app.register_blueprint(yakiList_route.app)
app.register_blueprint(schoolList_route.app)
app.register_blueprint(mannerList_route.app)
app.register_blueprint(haikuList_route.app)
app.register_blueprint(imageList_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=1000)