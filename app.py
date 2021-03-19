from api import FastCustomAPI, FlaskCustomAPI

api = FastCustomAPI(__name__)

@api.post("/posttest")
def posttest():
    data = {"name" : "Susmit"}
    return api.resp_wrapper(
        mssg = "Test",
        data = data
    )

@api.get("/postget")
def postget():
    data = {"name" : "Susmit"}
    return api.resp_wrapper(
        mssg = "Test",
        data = data
    )


if __name__ == "__main__":
    api.run()
