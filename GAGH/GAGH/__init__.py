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

        app.config['db_location'] = config.get("db", "location") + config.get("db", "name")
        print(app.config['db_location'])
        app.config['html_location'] = config.get("html", "location")

    except:
        app.logger.error("Could not read configs from: ", config_location)

    from GAGH.data.data import bp as data_bp

    from GAGH.main.routes import bp as main_bp
    from GAGH.reviews.routes import bp as reviews_bp
    from GAGH.submit.routes import bp as submit_bp
    from GAGH.user.routes import bp as user_bp

    app.register_blueprint(data_bp)

    app.register_blueprint(main_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(user_bp)


init(app)
log_init(app)

if __name__ == "__main__":
    init(app)
    log_init(app)

    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
