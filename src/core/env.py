from functools import lru_cache # so our env file doesnot relode a bunch of times

from pathlib import Path 
from decouple import config as decouple_config, Config, RepositoryEnv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_DIR=BASE_DIR.parent # mean we are at now src folder
ENV_FILE_PATH=PROJECT_DIR / ".env"

@lru_cache
def get_config():
    if ENV_FILE_PATH.exists():
        return Config(RepositoryEnv(str(ENV_FILE_PATH)))
    return decouple_config

config=get_config()

print(f"ENV_FILE_PATH exists: {ENV_FILE_PATH.exists()}")
