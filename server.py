from http.server import SimpleHTTPRequestHandler, HTTPServer
import os


class FrontController(SimpleHTTPRequestHandler):  # Written by ChatGPT
    def do_GET(self):
        # Only rewrite if the path is a directory or doesn't exist
        file_path = self.path.lstrip("/")
        if self.path.startswith("/trackers/") and not os.path.isfile(file_path):
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    HTTPServer(("localhost", 8080), FrontController).serve_forever()
