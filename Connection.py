import requests
import json
import sys
from flask import Flask, request
from multiprocessing import Process
import webbrowser
import pickle
from datetime import datetime
from flask_script import Manager, Server
import time

SUCCESS_COLOR = "\033[92m"
ERROR_COLOR = "\033[91m"
END_COLOR = "\033[0m"
TIME_FORMAT = "%y-%m-%d"


class MissingConfigError(Exception):
    """Exception raised for missing config field.

    Attributes:
        message
    """

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class Connection:
    def __init__(self, conf_file = "app_conf.json") -> None:
        self.config_required_attrs = ['APP_ID', 'APP_KEY', 'ACESS_TOKEN', "CODE_URL"]
        self.load_conf(conf_file)
        try:
            self.load_token()
            if (datetime.now() - self.token_reg_date).days >= 60:
                raise Exception
            print(f"{SUCCESS_COLOR}Success!{END_COLOR} token info successfully loaded.")
        except:
            error = f"{ERROR_COLOR}Error:{END_COLOR} Token not existing or expired. Please run connect method"
            print(error, file=sys.stderr)

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
        self.validate_config()
        url = f"https://ludopedia.com.br/oauth?app_id={self.APP_ID}&&redirect_uri={self.CODE_URL}"


        # class CustomServer(Server):
        #     def __call__(self, app, *args, **kwargs):
        #         custom_call()
        #         return Server.__call__(self, app, *args, **kwargs)

        app = Flask(__name__)

        # manager = Manager(app)
        # Remeber to add the command to your Manager instance
        # manager.add_command('runserver', CustomServer())

        # @manager.command
        # def runserver():
        #     app.run()
        #     p = Process(target=custom_call)
        #     p.start()

        @app.route("/")
        def hello_world():
            self.code = request.args['code']
            return self.authenticate(self.code)
            # return "Please go back to your application"

        def custom_call():
            # print("requesting")
            # time.sleep(3)
            # print("requesting")
            h = {
                "Host": "ludopedia.com.br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https//ludopedia.com.br",
                "Connection": "keep-alive",
            }
            r = requests.post(url, data={"autorizar": 1}, headers=h)
            app.logger.error(r.text)
        # manager.run()
        custom_call()
        app.run()
        # p = Process(target=custom_call)
        # p.start()


        # print("--------------------------------------------")
        # print(f"Please go to this url in your web browser {url}")
        # print("--------------------------------------------")
        # webbrowser.open(url, new=2)

    def authenticate(self, code):
        url = "https://ludopedia.com.br/tokenrequest"
        response = requests.post(url, data={"code":code})
        self.access_token =  json.loads(response.text)["access_token"]
        self.save_token(self.access_token)

    def load_token(self):
        with open('data.pickle', 'rb') as f:
            access_info = pickle.load(f)
            self.access_token = access_info['token']
            self.token_reg_date = datetime.strptime(access_info['token_reg_date'], TIME_FORMAT)
            return self.access_token, self.token_reg_date

    def save_token(self, access_token):
        with open('data.pickle', 'wb') as f:
            pickle.dump({"token": access_token, "token_reg_date": datetime.now().strftime(TIME_FORMAT)}, f, pickle.HIGHEST_PROTOCOL)

    def validate_config(self):
        errors = []
        attrs = self.config_required_attrs
        for attr in attrs:
            if not hasattr(self, attr):
                errors.append(f"Configuration {attr} is missing, please add it to your config file and reload the config.")
        if len(errors) > 0:
            raise MissingConfigError("\n".join(errors))

    def __str__(self) -> str:
        conf = "\n".join(map(lambda x: f"{x}: {getattr(self, x)}", self.config_required_attrs))
        return f"config file for Ludopedia API:\n {conf}"

if __name__ == '__main__':
    conn = Connection()
    conn.connect()