"""
Flask Server
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
#main
from main.src import wordList2_route
from main.src import nameList_route
from main.src import nameList2_route
from main.src import yakiList_route
from main.src import yakiList2_route
from main.src import schoolList_route
from main.src import mannerList_route
from main.src import haikuList_route
from main.src import imageList_route
from main.src import kinshiList_route

#file
from file.src import karaokeList_route
from file.src import radioList_route
from file.src import ssbuList_route
from file.src import voiceList_route
from file.src import support_route
from file.src import movieList_route
from file.src import obaRadioList_route

#scraper
from scraper.src import twitter_route
from scraper.src import holosong_route
from scraper.src import holomovie_route
from scraper.src import holoarchive_route

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
app.register_blueprint(nameList2_route.app)
app.register_blueprint(yakiList_route.app)
app.register_blueprint(yakiList2_route.app)
app.register_blueprint(schoolList_route.app)
app.register_blueprint(mannerList_route.app)
app.register_blueprint(haikuList_route.app)
app.register_blueprint(imageList_route.app)
app.register_blueprint(kinshiList_route.app)
#file
app.register_blueprint(karaokeList_route.app)
app.register_blueprint(radioList_route.app)
app.register_blueprint(ssbuList_route.app)
app.register_blueprint(voiceList_route.app)
app.register_blueprint(support_route.app)
app.register_blueprint(movieList_route.app)
app.register_blueprint(obaRadioList_route.app)
#scraper
app.register_blueprint(twitter_route.app)
app.register_blueprint(holosong_route.app)
app.register_blueprint(holomovie_route.app)
app.register_blueprint(holoarchive_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)