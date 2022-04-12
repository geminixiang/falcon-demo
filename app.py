import falcon
import json
import csv
import arrow
import gevent
from gevent import socket, monkey


monkey.patch_all()


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

    def on_post(self, req, resp):
        num = req.media.get("num")
        resp.media = {
            "You post number is": num
        }
        resp.status = falcon.HTTP_200


class Timestamp:
    def on_get(self, req, resp):
        """GET SYSTEM TIME"""
        print(req.method, req.host, req.port)
        payload = {}
        payload['utc'] = arrow.utcnow().to('Asia/Taipei'). \
            format('YYYY-MM-DD HH:mm:ss')
        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_200


class Crawler(object):
    def on_get(self, req, resp):
        """request 10 website at the same time"""
        urls = ['www.google.com', 'www.example.com', 'www.python.org',
                'www.netflix.com', 'hackmd.io', 'medium.com',
                'www.bing.com', 'aws.amazon.com', 'www.ithome.com.tw',
                'www.wikipedia.org']
        jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
        _ = gevent.joinall(jobs, timeout=5)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps([job.value for job in jobs])


class Factorial(object):

    def number_loop(self, end):
        if end == 1:
            return 1
        if end < 1:
            return "NA"

        return end * self.number_loop(end - 1)

    def on_get(self, req, resp, **kwargs):
        end = kwargs['end']

        if not end.isdigit():
            raise falcon.HTTPBadRequest(title='Param must be a NUMBER')

        end = int(end) + 1
        jobs = [gevent.spawn(self.number_loop, i) for i in range(1, end)]
        gevent.joinall(jobs, timeout=5)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps([job.value for job in jobs])


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
        for i in range(n + 1):
            writer.writerow((i, current))
            previous, current = current, current + previous

            yield from stream.result
            stream.clear()

    def on_get(self, req, resp):
        resp.content_type = 'text/csv'
        resp.downloadable_as = 'report.csv'
        resp.stream = self.fibonacci_generator()


def create():
    app = falcon.App()
    app.add_route('/info', About())
    app.add_route('/time', Timestamp())
    app.add_route('/crawler', Crawler())
    app.add_route('/download', DownloadFile())
    app.add_route('/factorial/{end}', Factorial())
    return app


app = create()
