import requests
import json
import sys

SUCCESS_COLOR = "\033[92m"
ERROR_COLOR = "\033[91m"
END_COLOR = "\033[0m"


class MissingConfigError(Exception):
    """Exception raised for missing config field.

    Attributes:
        message
    """

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class Connnection:
    def __init__(self, conf_file = "app_conf.json") -> None:
        self.load_conf(conf_file)

    def load_conf(self, conf_file = "app_conf.json"):
        try:
            with open(conf_file) as conf:
                conf_dict = json.load(conf)
                for k, v in conf_dict.items():
                    setattr(self, k, v)
            self.validate_config()
        except Exception as e:
            error = f"{ERROR_COLOR}Error:{END_COLOR} Could not load config file on path {conf_file}."
            error = f"{error}\nDouble check the path and make sure it´s a json file."
            error = f"{error}\n{e}"
            print(error, file=sys.stderr)
            return
        print(f"{SUCCESS_COLOR}Success!{END_COLOR} {conf_file} successfully loaded {self}")

    def connect(self):
        pass

    def validate_config(self):
        errors = []
        attrs = ['APP_ID', 'APP_KEY', 'ACESS_TOKEN']
        for attr in attrs:
            if not hasattr(self, attr):
                errors.append(f"Configuration {attr} is missing, please add it to your config file and reload the config.")
        if len(errors) > 0:
            raise MissingConfigError("\n".join(errors))


            


    def __str__(self) -> str:
        try:
            conf = f"APP_ID: {self.APP_ID}\n APP_KEY: {self.APP_KEY}\n ACESS_TOKEN: {self.ACESS_TOKEN}"
        except Exception as e:
            conf = e
        return f"config file for Ludopedia API:\n {conf}"


if __name__ == '__main__':
    conn = Connnection()