from typing import  Dict
from abc import ABC, abstractmethod
from fastapi.responses import JSONResponse
from flask import jsonify, Flask
import uvicorn
from fastapi import FastAPI

class ResponseWrapper(ABC):
    @abstractmethod
    def __call__(self, mssg : str, data : Dict, success : bool = True):

        pass

class FastAPIResponseWrapper(ResponseWrapper):
    def __call__(self, mssg : str, data : Dict, success : bool  = True):
        return JSONResponse({
            "success" : success,
            "mssg" : mssg,
            "data" : data
        })

class FlaskAPIResponseWrapper(ResponseWrapper):
    app = Flask(__name__)
    def __call__(self, mssg : str, data : Dict, success : bool = True):
        
        with self.app.app_context():
            return jsonify({
                "success" : success,
                "mssg" : mssg,
                "data" : data
            })


class API(ABC):
    @abstractmethod
    def __init__(self, name):
        pass
    @abstractmethod
    def get(self,path):
        pass
    @abstractmethod
    def post(self, path):
        pass
    @abstractmethod
    def run(self):
        pass

class FastCustomAPI(API):
    def __init__(self, name):
        self.app = FastAPI()
        self.resp_wrapper = FastAPIResponseWrapper()

    def get(self,path):
        return self.app.get(path)

    def post(self, path):
        return self.app.post(path)
    
    def run(self):
        uvicorn.run(self.app,host="0.0.0.0",port=5000,proxy_headers=True)


class FlaskCustomAPI(API):
    def __init__(self, name):
        self.app = Flask(name)
        self.resp_wrapper = FlaskAPIResponseWrapper()

    def get(self,path):
        return self.app.route(path, methods=["GET"])

    def post(self, path):
        return self.app.route(path, methods=["POST"])

    def run(self):
        self.app.run("127.0.0.1",port=5000)