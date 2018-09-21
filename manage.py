'''
    manage.py

    Server start module
'''

import os
from app import create_app
from flask_script import Manager, Shell, Command, Option
from pymongo import MongoClient


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug = True

manager = Manager(app)

'''# for mongodb use
mongo_url = ('mongodb://%s:%s@ds028310.mlab.com'
             ':28310/tudev_checkout' % (app.config['DB_USER'],
                                        app.config['DB_PASS']))
client = MongoClient(mongo_url, connect=False)
'''


def make_shell_context():
    return dict(app=app)

@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=1337)
@manager.option('-w', '--workers', dest='workers', type=int, default=4)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers,
                'timeout': 120
            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
