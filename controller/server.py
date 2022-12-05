from flask import Flask

# Serve a flask server
def serve(status, server_port):
    app = Flask(__name__)

    @app.route('/status')
    def get_status():
        return dict(status)

    app.run(host='0.0.0.0', port=server_port, debug=False, use_reloader=False)
