import falcon
import json
import csv
import arrow
import gevent
from gevent import socket


def number_loop(end):
    result = 1
    if end == 1:
        return 1
    for i in range(1, end):
        result *= i
    return result


class About:
    def on_get(self, req, resp):
        """Handle GET requests."""
        quote = {
            'author': 'Gemini Xiang',
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
        }

        resp.media = quote


class Timestamp:
    def on_get(self, req, resp):
        """GET SYSTEM TIME"""
        payload = {}
        payload['utc'] = arrow.utcnow().format('YYYY-MM-DD HH:mm:SS')
        resp.body = json.dumps(payload)
        resp.status = falcon.HTTP_200


class Ping(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps('pong!')


class Crawler(object):
    def on_get(self, req, resp):
        """gevent spawn a little job"""
        urls = ['www.google.com', 'www.example.com', 'www.python.org']
        urls *= 100
        jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
        _ = gevent.joinall(jobs, timeout=2)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps([job.value for job in jobs])


class Factorial(object):

    def on_get(self, req, resp, end):
        jobs = [gevent.spawn(number_loop, i) for i in range(1, int(end) + 1)]
        _ = gevent.joinall(jobs, timeout=2)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps([job.value for job in jobs])

    def on_post(self, req, resp, end):
        num = req.media.get("num")
        resp.media = {
            "message": num
        }
        resp.status = falcon.HTTP_200


class DownloadFile:

    class PseudoTextStream:
        def __init__(self):
            self.clear()

        def clear(self):
            self.result = []

        def write(self, data):
            self.result.append(data.encode())

    def fibonacci_generator(self, n=1000):
        stream = self.PseudoTextStream()
        writer = csv.writer(stream, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('n', 'Fibonacci Fn'))

        previous = 1
        current = 0
        for i in range(n+1):
            writer.writerow((i, current))
            previous, current = current, current + previous

            yield from stream.result
            stream.clear()

    def on_get(self, req, resp):
        resp.content_type = 'text/csv'
        resp.downloadable_as = 'report.csv'
        resp.stream = self.fibonacci_generator()


app = falcon.App()


app.add_route('/', About())
app.add_route('/time', Timestamp())
app.add_route('/ping', Ping())
app.add_route('/crawler', Crawler())
app.add_route('/download', DownloadFile())
app.add_route('/factorial/{end}', Factorial())
