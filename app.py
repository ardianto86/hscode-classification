from flask import Flask, redirect, url_for, request
from redis import Redis
import search.InterfaceManager

VERSION = "v1"

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

#GET http://127.0.0.1:5000/v1/search
@app.route( "/"+VERSION+ "/search",methods = ['GET'])
def search():
    manager = search.InterfaceManager()
    return manager.classify(request.args.get('search'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)