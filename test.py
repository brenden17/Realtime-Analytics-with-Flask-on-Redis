import unittest
from datetime import datetime, timedelta

from redis import Redis

from extensions import *

redis = Redis()

class EventBitmapTestCase(unittest.TestCase):
    def setUp(self):
        self.EA = EventAnalytics('test')

    def _tearDown(self):
        self.EA.delete_all_events('test')

    def test_create_event(self):
        create_event(1, 'test')
        create_event(2, 'test')
        d = datetime.today() - timedelta(days=4)
        create_event(3, 'test', target_time=d)
        d = datetime.today() - timedelta(days=3)
        create_event(4, 'test', target_time=d)

    def _test_all_events(self):
        EA = EventAnalytics('test')
        EA.fetch_daily(last=7)

if __name__ == '__main__':
    unittest.main()