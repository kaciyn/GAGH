from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def root():
    return render_template('/html/base.html'),200

    @app.route('/submit/')
def submit():
    return render_template('/html/submit.html'),200

    
    @app.route('/config/')
def config():
    strg = []
    strg.append('Debug: %s' % app.config['DEBUG'])
    strg.append('port:'+app.config['port'])
    strg.append('url:'+app.config['url'])
    strg.append('ip_address:'+app.config['ip_address'])
    return '\t'.join(str)

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

    except:
        print "Could not read configs from: ", config_location

init(app)

if __name__ == '__main__':
    init(app)
    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
