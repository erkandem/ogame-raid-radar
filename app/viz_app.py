import flask

app = flask.Flask('oGame NSE')


@app.route('/')
def index_page():
    return flask.render_template('index.html')


@app.route('/', methods=['POST'])
def response():
    return flask.render_template('response.html')


if __name__ == '__main__':
    app.run()
