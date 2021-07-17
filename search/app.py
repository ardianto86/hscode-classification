from flask import Flask, redirect, url_for, request
from redis import Redis
import InterfaceManager
import json

VERSION = "v1"

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

###############################
#        CLASS OBJECT         #
###############################
class InterfaceManager:
    def classify(self,json_string):
        data = json.loads(json_string)
        item = data["search"]
        print(item)
        # The search item has been found! Return now
        results = [123,1245,13567]
        return json.dumps(self.__Deserialize(results))
        
    def __Deserialize(self,results):
        return 	{"results": results}	

###############################
#        UNIT TEST            #
###############################
if __name__ == "__main__" :
    manager = InterfaceManager()
    message = manager.classify(json.dumps({"search":"LAMB CHOP"}))
    print(message)


###############################
#       REST API          #
###############################
#GET http://127.0.0.1:5000/v1/search
@app.route( "/"+VERSION+ "/search",methods = ['GET'])
def search():
    manager = InterfaceManager()
    return json.dumps({"status":request.args.get('search')})
    #return manager.classify(request.args.get('search'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)