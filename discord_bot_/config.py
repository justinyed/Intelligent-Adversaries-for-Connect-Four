import os
import json


class Config:

    def __init__(self, file_path):
        self.TOKEN = None
        self.file_path = file_path
        if self.read_token_environment_variable() is not None:
            print("[INFO] Getting discord token from DISCORD_TOKEN env variable")
            Config.TOKEN = self.read_token_environment_variable()
        else:
            print("[INFO] Getting discord token from config file")
            Config.TOKEN = self.read_json_config()

        if Config.TOKEN is None:
            exit("ERROR - unable to get TOKEN from config")

    def __del__(self):
        pass

    def read_token_environment_variable(self):
        env_token = os.environ.get('DISCORD_TOKEN', None)

        if env_token is not None and len(env_token) > 10:
            return env_token

        return None

    def read_json_config(self, ):
        Config.CONFIG_FILE = os.path.join(self.file_path)
        deserialised_json_config = Config.deserialise_json_file(Config.CONFIG_FILE)
        return deserialised_json_config.get('Token', None)

    @staticmethod
    def deserialise_json_file(json_file_path: str) -> dict:
        # Weak file check, simply check file extension is json..
        if json_file_path[-5:] != ".json":
            raise ValueError('File doesn\'t have a \'json\' extension')

        if not os.path.isfile(json_file_path):
            raise FileNotFoundError(json_file_path + " Not Found")

        with open(json_file_path) as file:
            data = json.load(file)

        return data
