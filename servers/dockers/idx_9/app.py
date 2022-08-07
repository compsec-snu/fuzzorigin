import flask
import time
import logging
 
logging.basicConfig(filename = "/data/log.txt", level = logging.DEBUG)

app = flask.Flask(__name__)

@app.route('/sop/<name>')
def sop_send(name):
    with open(f"/data/sop/{name}") as f:
        html = f.read()

    response = flask.Response(html)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@app.route('/<name>')
def send(name):
    # return flask.send_from_directory('.', name)
    logging.info(f"[LOG] {name}")
    r = flask.make_response(flask.send_from_directory('/data', name))
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    r.set_cookie('userID', 'parent')
    return r

@app.route('/svg/<name>')
def svg_send(name):
    with open("/data/svg/template.svg") as f:
        html = f.read()
    html = html.replace("<name>", name.split(".")[0])
    r = flask.Response(html, mimetype='image/svg+xml')
    return r

@app.route('/svg_parent/<name>')
def svg_parent_send(name):
    with open("/data/svg/template.svg") as f:
        html = f.read()
    html = html.replace("<name>", f"{name.split('.')[0]}.parentNode")
    r = flask.Response(html, mimetype='image/svg+xml')
    return r

@app.route('/')
def hello_world():
    return 'Hello, idx_9!'

if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0", port=7009)
    #app.run(port=7000)
