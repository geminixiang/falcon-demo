from falcon import testing
import random
import app


class SetUpTest(testing.TestCase):
    def setUp(self):
        super(SetUpTest, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.App` instance.
        self.app = app.create()


class ApiTest(SetUpTest):
    """
        app.add_route('/info', About())
    app.add_route('/time', Timestamp())
    app.add_route('/crawler', Crawler())
    app.add_route('/download', DownloadFile())
    app.add_route('/factorial/{end}', Factorial())
    """
    def test_info_get(self):
        doc = {"author": "Gemini Xiang", "quote": "I've always been more interested in the future than in the past."}

        result = self.simulate_get('/info')
        self.assertEqual(result.status, '200 OK')
        self.assertEqual(result.json, doc)

    def test_info_post(self):
        num = random.randint(1, 100)
        doc = {'num': num}

        result = self.simulate_post('/info', json=doc)
        self.assertEqual(result.status, '200 OK')
        self.assertTrue(True if "You post number is" in result.json else False)
        self.assertEqual(result.json["You post number is"], num)

    def test_time_get(self):
        result = self.simulate_get('/time')
        self.assertEqual(result.status, '200 OK')
        self.assertTrue(True if "utc" in result.json else False)

    def test_crawler_get(self):
        result = self.simulate_get('/crawler')
        self.assertEqual(result.status, '200 OK')
        self.assertIs(type(result.json), list, msg=type(result.json))

    def test_download_get(self):
        result = self.simulate_get('/download')
        self.assertEqual(result.status, '200 OK')
        
        print(result)
        # self.assertGreaterEqual(result.headers, 5000, msg=result.cookies)
