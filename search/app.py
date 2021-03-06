from flask import Flask, redirect, url_for, request, render_template, make_response
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
from flask_bootstrap import Bootstrap

VERSION = "v1"
SEARCH = 'search'

THIS_SCRIPT_PATH = os.path.dirname(__file__)

flask_app = Flask(__name__)
app = Api(app = flask_app)
bootstrap = Bootstrap(flask_app)

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
        ITEM = "item"
        RESULT = "result"
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
        items = []
        result = {}
        datas = []
        type = self.config[DEFAULT]
        model_file =  self.config[MODEL_FILE]

        if(os.path.isfile(item)):
            csv_data = pd.read_csv(item)
        else:
            items.append(item)

        for item in items:
            result[ITEM] = item
            result[RESULT] = []
            if(type == EnumSearches.KNN):
                data = {}
                knn_loaded_model = pickle.load(open(model_file["knn"], 'rb'))
                new_series = pd.Series(item)
                predict_results = knn_loaded_model.predict(new_series).tolist()
                for predict_result in predict_results:
                    data[HSCODE] = predict_result
                    data[DESCRIPTION] = "A single product"
                    data[PROBABILITY] = 0.9
                    result[RESULT].append(data)
            
            if(type == EnumSearches.Mock):
                data = {}
                data[HSCODE]        = 133456
                data[DESCRIPTION]   = "A single product"
                data[PROBABILITY]   = 0.9
                result[RESULT].append(data)
            datas.append(result)

        response[DATA] = datas
        response[STATUS] = self.get_status()    
        return json.dumps(response)

    def classify2(self,item):
        print(item)
        # The search item has been found! Return now
        return "<h1>someresult</h1>"

manager = ClassifyManager()

###############################
#       REST API          #
###############################
PARAMS_SEARCH_GET_JSON = { 'input': 'Specify input string or CSV file to search the HS code' } 

#GET http://127.0.0.1:5000/v1/search/<input>
@name_space.route("/"+VERSION+ "/"+ SEARCH + "/<input>")
class search_input(Resource):
    @app.doc(responses=STATUS_SEARCH_GET, 
			 params=PARAMS_SEARCH_GET_JSON)
    def get(self,input):
        return manager.classify(input)

#@name_space.route("/"+VERSION+ "/"+ SEARCH + "/utility")
#class search_utility(Resource):

@app.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@app.route('/index')
class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

@app.route('/filter')
class Filter(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('filter.html'),200,headers)

###############################
#        UNIT TEST            #
###############################
if __name__ == "__main__" :
    flask_app.run(host="0.0.0.0", debug=True)

