import Majjaka_eProcure.wsgi

SCRIPT_NAME = 'home/a98zy7m9c1gd/repositories/procurezy_deploy'


class PassengerPathInfoFix(object):
    """
    Sets PATH_INFO from REQUEST_URI because Passenger doesn't provide it.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME

        request_uri = unquote(environ['REQUEST_URI'])
        script_name = unquote(environ.get('SCRIPT_NAME', ''))
        offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
        environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
        return self.app(environ, start_response)


application = Majjaka_eProcure.wsgi.application
application = PassengerPathInfoFix(application)
