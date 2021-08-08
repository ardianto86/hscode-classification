from flask import Flask, redirect, url_for, request
import werkzeug 
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api, Resource
import json
import pickle
from pandas import pandas as pd
import numpy as np
import enum
from enum import IntEnum
import os

VERSION = "v1"
SEARCH = 'search'

THIS_SCRIPT_PATH = os.path.realpath(__file__)

flask_app = Flask(__name__)
app = Api(app = flask_app)

name_space = app.namespace(SEARCH, description = 'To access search engine API')

###############################
#     SEARCH CATEGORIZATION   #
###############################
class EnumSearches(enum.Enum):
    Mock = 1
    KNN = 2

class EnumStatus(IntEnum):
    OK = 200
    SEARCH_INVALID_ARG                          = 40001
    SEARCH_NOT_FOUND_RESULT                     = 40101
    SEARCH_INTERNAL_NOT_FOUND_MODEL             = 41001
    SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION     = 41002
     
STATUS_SEARCH_GET = {}
STATUS_SEARCH_GET[int(EnumStatus.OK)]                                        = 'OK'
STATUS_SEARCH_GET[int(EnumStatus.SEARCH_INVALID_ARG)]                        = 'Invalid Argument'
STATUS_SEARCH_GET[int(EnumStatus.SEARCH_NOT_FOUND_RESULT)]                   = 'HS code not found'
STATUS_SEARCH_GET[int(EnumStatus.SEARCH_INTERNAL_NOT_FOUND_MODEL)]           = 'Internal error, model file not found'
STATUS_SEARCH_GET[int(EnumStatus.SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION)]   = 'Internal error, configuration file not found'

print(STATUS_SEARCH_GET)

###############################
#        CLASS OBJECT         #
###############################
class ClassifyManager:
    def __init__(self):
        CONFIGURATION = THIS_SCRIPT_PATH + "\configuration\setting.json"  
        if(os.path.isfile(CONFIGURATION)):
            self.status = EnumStatus.OK
            json.load(CONFIGURATION)
        else: self.status = EnumStatus.SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION

    def classify(self,item, type):
        if(type == EnumSearches.KNN):
            knn_loaded_model = pickle.load(open('model_knn.sav', 'rb'))
            new_series = pd.Series(item)
            predict_result = knn_loaded_model.predict(new_series).tolist()
            return predict_result
        
        if(type == EnumSearches.Mock):
            return [1,2,3]

###############################
#        UNIT TEST            #
###############################
if __name__ == "__main__" :
    manager = ClassifyManager()
    message = manager.classify("TEST",EnumSearches.Mock)
    print(message)


###############################
#       REST API          #
###############################
PARAMS_SEARCH_GET_JSON = { 'input': 'Specify the HS code which is provided by user' } 

#GET http://127.0.0.1:5000/v1/search/<input>
@name_space.route("/"+VERSION+ "/"+ SEARCH + "/<input>")
class SearchSingle(Resource):
    @app.doc(responses=STATUS_SEARCH_GET, 
			 params=PARAMS_SEARCH_GET_JSON)
    def get(self,input):
        print(input)
        manager = ClassifyManager()
        results = manager.classify(input,EnumSearches.KNN)
        return json.dumps({"results":results})

#GET http://127.0.0.1:5000/v1/search/mock/<input>
@name_space.route("/"+VERSION+ "/"+ SEARCH + "/mock/<input>")
class SearchSingleMock(Resource):
    @app.doc(responses=STATUS_SEARCH_GET, 
			 params=PARAMS_SEARCH_GET_JSON)
    def get(self,input):
        print(input)
        manager = ClassifyManager()
        results = manager.classify(input,EnumSearches.Mock)
        return json.dumps({"results":results})

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True)