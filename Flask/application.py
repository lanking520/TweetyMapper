from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS, cross_origin
# from read_data import DataReader
from essearch import ESSearch

# EB looks for an 'application' callable by default.
application = Flask(__name__)
CORS(application)
# pre-load fixed tweets
# def pre_load_fixed_data():
#     keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
#     data = DataReader()
#     return data.read("static/data/tweets.txt", keywords)

# # tweets_json = pre_load_fixed_data()

essearch = ESSearch()

@application.route('/')
def index():
    return render_template('index.html')

# @application.route('/searchf/')
# @application.route('/searchf/<keyword>')
# def searchf(keyword=None):
#     if keyword is None:
#         to_return = jsonify(**tweets_json)
#     else:
#         tweets_of_keyword = {keyword: []}
#         if keyword in tweets_json:
#             tweets_of_keyword = {keyword: tweets_json[keyword]}
#         to_return = jsonify(**tweets_of_keyword)
#     return to_return

@application.route('/search',methods=['POST'])
def search():
    data = request.get_json()
    if data["keyword"]:
        to_return = essearch.draftsearch(data["keyword"])
    else:
    	to_return = {}
    return jsonify(**to_return)
    # else:
    #     search_result = essearch.search(keyword)
    #     to_return = jsonify(**search_result)
    # return to_return

@application.route('/img/<filename>')
# Fix the problem of finding images
def get_image(filename=None):
    return send_file('static/img/'+filename, mimetype='image/png')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.threaded = True
    application.run()
