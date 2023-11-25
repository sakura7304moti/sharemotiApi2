"""
Flask Server
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
#main
from main.route import wordList2_route
from main.route import nameList_route
from main.route import yakiList_route
from main.route import schoolList_route
from main.route import mannerList_route
from main.route import haikuList_route
from main.route import imageList_route

#file
from file.route import karaokeList_route
from file.route import radioList_route
from file.route import ssbuList_route
from file.route import voiceList_route
from file.route import support_route

#scraper
from scraper.route import twitter_route
from scraper.route import holosong_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
register blueprint
"""
#main
app.register_blueprint(wordList2_route.app)
app.register_blueprint(nameList_route.app)
app.register_blueprint(yakiList_route.app)
app.register_blueprint(schoolList_route.app)
app.register_blueprint(mannerList_route.app)
app.register_blueprint(haikuList_route.app)
app.register_blueprint(imageList_route.app)
#file
app.register_blueprint(karaokeList_route.app)
app.register_blueprint(radioList_route.app)
app.register_blueprint(ssbuList_route.app)
app.register_blueprint(voiceList_route.app)
app.register_blueprint(support_route.app)
#scraper
app.register_blueprint(twitter_route.app)
app.register_blueprint(holosong_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)