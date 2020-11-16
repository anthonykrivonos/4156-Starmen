import os
import sys
from os.path import join, realpath, dirname

sys.path.append(join(os.getcwd(), '..'))

from typing import List

from dotenv import load_dotenv

env_path = join(dirname(realpath(__file__)), '../../.env')
load_dotenv(dotenv_path=env_path)

class Env:
    @staticmethod
    def PORT() -> str:
        return os.getenv("PORT")

    @staticmethod
    def UPMED_PRIVATE_KEY() -> str:
        return os.getenv("UPMED_PRIVATE_KEY")

    @staticmethod
    def FIREBASE_PRIVATE_KEY() -> str:
        return os.getenv("FIREBASE_PRIVATE_KEY")

    @staticmethod
    def TWILIO_ACCOUNT_SID() -> str:
        return os.getenv("TWILIO_ACCOUNT_SID")

    @staticmethod
    def TWILIO_API_KEY_SID() -> str:
        return os.getenv("TWILIO_API_KEY_SID")

    @staticmethod
    def TWILIO_API_KEY_SECRET() -> str:
        return os.getenv("TWILIO_API_KEY_SECRET")

    @staticmethod
    def TWILIO_AUTH_TOKEN() -> str:
        return os.getenv("TWILIO_AUTH_TOKEN")

# Ensure .env file is up to date, or exit promptly
missing_envs: List[str] = []
for key in Env.__dict__.keys():
    val = Env.__dict__[key]
    try:
        if not key.startswith("__") and callable(val.__get__(Env)):
            if not val.__get__(Env)():
                missing_envs.append(key)
    except TypeError as e:
        pass

if missing_envs:
    sys.exit("upmed-appointment/.env file not up to date. Missing %s!" % ", ".join(missing_envs))
