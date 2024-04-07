from fastapi import FastAPI
from config import settings

#from app.Utils.DatabaseTests import DatabaseTests
#do_tests = DatabaseTests.run_test()


app = FastAPI()


def create_app(settings: Settings):
    pass