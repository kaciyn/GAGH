import configparser
import os

from flask import Flask
from GAGH.handlers.logger import log_init

app = Flask(__name__)
app.secret_key = os.urandom(24)

# INIT
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = "GAGH/etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")

    except:
        app.logger.error("Could not read configs from: ", config_location)

    from GAGH.main.routes import bp as main_bp

    app.register_blueprint(main_bp)
    print (app.url_map)

init(app)
log_init(app)

if __name__ == "__main__":
    init(app)
    log_init(app)

    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
