from woma.endpoints import Endpoint
from woma.router import Router


def say_hello(name):
    return 'Hello %s!\n' % name


def say_goodbye(name):
    return 'Goodbye %s!\n' % name


class GreetingController(object):
    def __init__(self, greeter):
        self.greeter = greeter

    def __call__(self, request, response):
        name = request.kwargs['name']
        response.text = self.greeter(name)
        return response


hello_controller = GreetingController(say_hello)
goodbye_controller = GreetingController(say_goodbye)

hello_endpoint = Endpoint(hello_controller)
goodbye_endpoint = Endpoint(goodbye_controller)

router = Router()
router.add('/hello/{name}', hello_endpoint)
router.add('/goodbye/{name}', goodbye_endpoint)
