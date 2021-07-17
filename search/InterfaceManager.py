import json

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