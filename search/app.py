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

THIS_SCRIPT_PATH = os.path.dirname(__file__)

flask_app = Flask(__name__)
app = Api(app = flask_app)

DESCRIPTION ='''
This API is the API libraries which is used to get the search result from the search engine
'''

name_space = app.namespace(SEARCH, description = DESCRIPTION)

###############################
#     SEARCH CATEGORIZATION   #
###############################
class EnumSearches(str,enum.Enum):
    Mock = "mock"
    KNN = "knn"

class EnumStatus(IntEnum):
    OK = 200
    SEARCH_INVALID_ARG                          = 40001
    SEARCH_NOT_FOUND_RESULT                     = 40101
    SEARCH_INTERNAL_NOT_FOUND_MODEL             = 41001
    SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION     = 41002
     
STATUS_SEARCH_GET = {}
STATUS_SEARCH_GET[str(EnumStatus.OK)]                                        = 'OK'
STATUS_SEARCH_GET[str(EnumStatus.SEARCH_INVALID_ARG)]                        = 'Invalid Argument'
STATUS_SEARCH_GET[str(EnumStatus.SEARCH_NOT_FOUND_RESULT)]                   = 'HS code not found'
STATUS_SEARCH_GET[str(EnumStatus.SEARCH_INTERNAL_NOT_FOUND_MODEL)]           = 'Internal error, model file not found'
STATUS_SEARCH_GET[str(EnumStatus.SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION)]   = 'Internal error, configuration file not found'


###############################
#        CLASS OBJECT         #
###############################
class ClassifyManager:
    def get_status(self):
        status = {}
        status["code"] = self.status
        status["message"] = STATUS_SEARCH_GET[str(self.status)]
        return status


    def __init__(self):
        CONFIGURATION = THIS_SCRIPT_PATH + "/configuration/setting.json"  
        print(CONFIGURATION)
        self.config = {}
        if(os.path.isfile(CONFIGURATION)):
            self.status = EnumStatus.OK
            self.config = json.load(open(CONFIGURATION))
        else: self.status = EnumStatus.SEARCH_INTERNAL_NOT_FOUND_CONFIGURATION

    def classify(self,item):
        #JSON DATA AND STATUS
        DATA = "data"
        STATUS = "status"
        
        #HS CODE OBJECT
        HSCODE = "hscode"
        DESCRIPTION = "description"
        PROBABILITY = "probability"

        #CONFIGURATION
        DEFAULT = "default"
        MODEL_FILE = "model_file"
        
        response = {}
        datas = []
        type = self.config[DEFAULT]
        model_file =  self.config[MODEL_FILE]
        print(type)
        print(EnumSearches.KNN)
        if(type == EnumSearches.KNN):
            data = {}
            knn_loaded_model = pickle.load(open(model_file["knn"], 'rb'))
            new_series = pd.Series(item)
            predict_results = knn_loaded_model.predict(new_series).tolist()
            for predict_result in predict_results:
                data[HSCODE] = predict_result
                data[DESCRIPTION] = "A single product"
                data[PROBABILITY] = 0.9
                datas.append(data)
        
        if(type == EnumSearches.Mock):
            data = {}
            data[HSCODE]        = 133456
            data[DESCRIPTION]   = "A single product"
            data[PROBABILITY]   = 0.9
            datas.append(data)

        response[DATA] = datas
        response[STATUS] = self.get_status()    
        return json.dumps(response)

###############################
#        UNIT TEST            #
###############################
if __name__ == "__main__" :
    manager = ClassifyManager()
    message = manager.classify("TEST")


###############################
#       REST API          #
###############################
PARAMS_SEARCH_GET_JSON = { 'input': 'Specify keyword to search the HS code' } 

#GET http://127.0.0.1:5000/v1/search/<input>
@name_space.route("/"+VERSION+ "/"+ SEARCH + "/<input>")
class SearchManager(Resource):
    @app.doc(responses=STATUS_SEARCH_GET, 
			 params=PARAMS_SEARCH_GET_JSON)
    def get(self,input):
        manager = ClassifyManager()
        return manager.classify(input)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True)