from flask import Flask, redirect, url_for, request
from redis import Redis
import json
import os

THIS_SCRIPT_PATH = os.path.realpath(__file__)

VERSION = "v1"

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

###############################
#        CLASS OBJECT         #
###############################
class ClassifyManager:
    def __init__(self):
        CONFIGURATION = THIS_SCRIPT_PATH + "\configuration\setting.json"  
        if(os.path.isfile(CONFIGURATION)):
            self.status
            json.load(CONFIGURATION)
    def classify(self,item):
        print(item)
        # The search item has been found! Return now
        return [2000,4000,6100]

###############################
#        UNIT TEST            #
###############################
if __name__ == "__main__" :
    manager = ClassifyManager()
    message = manager.classify("LAMBCHOP")
    print(message)


###############################
#       REST API          #
###############################
#GET http://127.0.0.1:5000/v1/search
@app.route( "/"+VERSION+ "/search",methods = ['GET'])
def search():
    manager = ClassifyManager()
    results = manager.classify(request.args.get('search'))
    return json.dumps({"results":results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)