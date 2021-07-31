from flask import Flask, redirect, url_for, request
import json
import pickle
from pandas import pandas as pd
import numpy as np

VERSION = "v1"

app = Flask(__name__)

###############################
#        CLASS OBJECT         #
###############################
class ClassifyManager:
    def classify(self,item):
        print(item)
        knn_loaded_model = pickle.load(open('model_knn.sav', 'rb'))
        new_series = pd.Series(item)
        predict_result = knn_loaded_model.predict(new_series).tolist()
        print(predict_result)
        # The search item has been found! Return now
        return [4,5,predict_result]

    def classify2(self,item):
        print(item)
        # The search item has been found! Return now
        return [1,2,3]


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
@app.route( "/"+VERSION+ "/search/<input>",methods = ['GET'])
def search(input):
    print('search HIT')
    manager = ClassifyManager()
    results = manager.classify(input)
    return json.dumps({"results":results})

@app.route( "/"+VERSION+ "/search2",methods = ['GET'])
def search2():
    print('search2 HIT')
    manager = ClassifyManager()
    results2 = manager.classify2("wine")
    return json.dumps({"results":results2})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)