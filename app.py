try:
    from flask import Flask, request
    from flask_restful import Resource,Api
    from flasgger import Swagger
    from flasgger.utils import swag_from
    from flask_restful_swagger import swagger
    import pickle
    import numpy

except Exception as e:
    print('Some Modules are missing {}'.format(e))



app = Flask(__name__)
api = Api(app)

api = swagger.docs(Api(app), apiVersion='0.1',api_spec_url='/docs')


from json import JSONEncoder
import json

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)





class MyApi(Resource):
    @swagger.model
    @swagger.operation(notes='some really good notes')
    @swag_from("swagger_config1.yml")
    def get(self,text):
        model = pickle.load(open('model.pkl', 'rb'))
        predict = model.predict([text])

        with open("numpyData.json", "w") as write_file:
            json.dump(predict, write_file, cls=NumpyArrayEncoder)
        
        with open("numpyData.json", "r") as read_file:
            print("Converting JSON encoded data into Numpy array")
            decodedArray = json.load(read_file)
            return{
            'Response':200,
            'Data':decodedArray
        }



        


api.add_resource(MyApi,'/sentiment_analysis/<string:text>')

if __name__ == '__main__':
    app.run(debug=True)