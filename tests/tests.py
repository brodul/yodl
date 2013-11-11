import unittest
import urllib2

from mock import patch
from pyramid import testing


def is_internet_on():
    try:
        urllib2.urlopen('http://www.youtube.com', timeout=1)
        return True
    except urllib2.URLError:
        pass
    return False

INTERNET = (is_internet_on(), "Can not access Youtube.com")


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        return
        from .views import main_view
        request = testing.DummyRequest()
        info = main_view(request)


class TaskTests(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_get_id(self, mock_popen):
        from yodl.tasks import get_id
        mock_popen.return_value.communicate.return_value = \
            ('id98765', '')

        self.assertEqual(
            get_id("http://www.youtube.com/watch?v=id98765"),
            'id98765'
        )

    #@unittest.skipUnless(*INTERNET)
    def test_get_id_implement(self):
        from yodl.tasks import get_id

        self.assertEqual(
            get_id("http://www.youtube.com/watch?v=c5NL76BXauY"),
            'c5NL76BXauY'
        )
