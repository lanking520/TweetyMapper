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
        if data.has_key("filter") and data["filter"]:
            to_return = essearch.draftsearch(data["keyword"],data["filter"])
        else:
            to_return = essearch.draftsearch(data["keyword"])
    else:
    	to_return = {}

    return jsonify(**to_return)
    # else:
    #     search_result = essearch.search(keyword)
    #     to_return = jsonify(**search_result)
    # return to_return

@application.route('/upload',methods=['GET','PUT,POST'])
def uploadES():
    # TODO: Add Functionalities to Upload to ES
    header = request.headers.get('x-amz-sns-message-type')
    try:
        data = json.loads(request.data)
    except:
        pass
    if header == 'SubscriptionConfirmation' and 'SubscribeURL' in data:
        url = data['SubscribeURL']
        response = requests.get(url)
        print "Subscribed to SNS: " + url
        return "Subscribed to SNS: " + url
    if header == 'Notification':
        print data['Message']
        search_result = esearch.upload(data['Message'])
        #new_tweets.append(data['Message'])
        return data['Message']
    return "ok"

@application.route('/updates', methods=['GET'])
def updates():
	if len(new_tweets) > 0:
		tweets = []
		while len(new_tweets) > 0 and len(tweets) < 10:
			tweets.append(new_tweets.pop(0))
		to_return = {"result":tweets}
	else:
		to_return = {"result":[]}
	return jsonify(**to_return)

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
