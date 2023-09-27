import os
from dotenv import load_dotenv
import json

load_dotenv()
env = os.environ

APP_NAME="FAST API"

# use proformance less stratgies
NOT_PRO_LESS = False

DATABASE_NAME = "default"

DATABASES = {
     "default": {
        "NAME": env.get("DEFAULT_DATABASE_NAME"),
        "USER": env.get("DEFAULT_DATABASE_USERNAME"),
        "PASSWORD": env.get("DEFAULT_DATABASE_PASSWORD"),
        "HOST": env.get("DEFAULT_DATABASE_HOST"),
        "PORT": env.get("DEFAULT_DATABASE_PORT")
    },
     "live": {
        "NAME": env.get("DEFAULT_DATABASE_NAME"),
        "USER": env.get("DEFAULT_DATABASE_USERNAME"),
        "PASSWORD": env.get("DEFAULT_DATABASE_PASSWORD"),
        "HOST": env.get("DEFAULT_DATABASE_HOST"),
        "PORT": env.get("DEFAULT_DATABASE_PORT")
    }
}

DEBUG = True

ALLOWED_HOSTS = json.loads(env.get("ALLOWED_HOSTS"))

DB = DATABASES[DATABASE_NAME]
# mysql://user:password@postgresserver:port/db
DATABASE_URL = f"mysql://{DB['USER']}:{DB['PASSWORD']}@{DB['HOST']}:{DB['PORT']}/{DB['NAME']}"
# print(DATABASE_URL)