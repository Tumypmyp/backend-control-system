from flask import Flask


def serve(status, server_port):
    app = Flask(__name__)

    @app.route('/status')
    def hello():
        return dict(status)

    app.run(host='0.0.0.0', port=server_port, debug=False, use_reloader=False)
