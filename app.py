from flask import Flask
from flask import request, Response
from functools import wraps
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')


def check_auth(fqdn, username, password):
    if fqdn in app.config['AUTH'].keys():
       return username == app.config['AUTH'][fqdn]['username'] \
              and password == app.config['AUTH'][fqdn]['password']
    else:
       return False

def authenticate():
    return Response (
            'Unauthorized :(\n', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        app.logger.debug(request.path)
        (root, action, domain, host) = str(request.path).split('/')
        fqdn = "{0}.{1}".format(host, domain)
        if not auth or not check_auth(fqdn, auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def updateMIAB(fqdn, ip):
    url = "{0}/dns/custom/{1}".format(app.config['URL'], fqdn)
    response = requests.put(url, data=ip,
                auth=(app.config['USER'], app.config['PASSWD']),
                headers={'content-type':'text/plain'}
               )

@app.route("/update/<domain>/<host>", methods=['POST'])
@requires_auth
def update(domain, host):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    else:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    fqdn = "{0}.{1}".format(host, domain)
    updateMIAB(fqdn, ip)
    return "Successfully updated {0}.{1} with value {2} :)\n".format(host, domain, ip)

@app.route('/')
def hello_world():
    return 'Hi! This is a MIAB dyndns server :P.'

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
