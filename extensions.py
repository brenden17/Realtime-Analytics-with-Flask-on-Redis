from redis import Redis
from random import getrandbits
from datetime import datetime, timedelta

from flask import session
from flask import Blueprint
from flask import render_template
from flask import Markup

redis = Redis()

class BitmapSession(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        session_id = session.sid
        user_id = redis.get(session_id)
        if not user_id:
            user_id = getrandbits(24)
            redis.set(session_id, user_id)
        # create event
        create_event(user_id, "buy")

        return response

def get_time_fmt(time_slot):
    if time_slot == 'daily':
        fmt = '%Y-%m-%d'
    elif time_slot == 'monthly':
        fmt = '%Y-%m'
    elif time_slot == 'hourly':
        fmt = '%Y-%m-%d-%H'
    else:
        fmt = '%Y-%m-%d'
    return fmt

ACTIONS = ('view', 'buy', 'cancel')

def create_key(action='view', time_slot='daily', target_time=None):
    time_fmt = get_time_fmt(time_slot)
    if not target_time:
        target_time = datetime.now()
    
    created_time = target_time.strftime(time_fmt)
    return 'event:{0}:{1}'.format(action, created_time)


def create_event(user_id, action='view', time_slot='daily', target_time=None):
    key = create_key(action, time_slot, target_time)
    try:
        redis.setbit(key, user_id, 1)
    except Exception, e:
        print(e)


class EventAnalytics(object):
    def __init__(self, actions=ACTIONS, time_slot='daily'):
        self.actions = actions
        self.time_slot = time_slot

    def fetch_daily(self, last=30):
        events = ','.join([self.get_event(action, day) for action in self.actions for day in range(last)])
        return '[{}]'.format(events)

    def get_event(self, action, last=30):
        d = datetime.today() - timedelta(days=last)
        key = create_key(action, self.time_slot, d)
        count = redis.bitcount(key)
        return '{"date":"%s", "action":"%s", "count":"%s"}' % \
                    (key.split(':')[2], action, count)

    def delete_all_events(self, action):
        events = redis.keys('event:{}:*'.format(action))
        if events:
            try:
                redis.delete(*events)
            except Exception, e:
                print(e)
            

class BitmapReport(object):
    """Graph report"""
    def __init__(self, actions=ACTIONS,
                        width='600',
                        height='250',
                        last=7,
                        daily=None, 
                        monthly=None,
                        graph='bar'
                        ):
        self.actions = actions
        self.graph = graph
        self.width = width
        self.height = height
        self.x = 'date'
        self.y = 'count'
        self.EA = EventAnalytics(actions)
        self.data = self.EA.fetch_daily(last)
        self.config = 'BitmapReport'

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def html(self):
        if self.graph == 'bar':
            base_html = 'AnalyticsRedis/{}.html'.format('bar')
        elif self.graph == 'pie':
            base_html = 'AnalyticsRedis/{}.html'.format('pie')
        else:
            base_html = 'AnalyticsRedis/{}.html'.format('bar')

        return Markup(self.render(base_html, rb=self))

def bitmap_analytics(*args, **kwargs):
    bitmap_report = BitmapReport(*args, **kwargs)
    return bitmap_report.html


class BitmapAnalytics(object):
    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):
        self.register_blueprint(app)
        app.add_template_global(bitmap_analytics)

    def register_blueprint(self, app):
        module = Blueprint(
            'AnalyticsRedis',
            __name__,
            template_folder='templates'
        )
        app.register_blueprint(module)
        return module

class AnalyticsRedis(object):
    def __init__(self, app):
        bs = BitmapSession(app)
        ba = BitmapAnalytics(app)