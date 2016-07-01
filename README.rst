Woma
====

Woma is a python web development framework.

It's an experiment in small, decoupled components with a single responsibility,
communicating through interfaces to solve larger problems. There's a big
emphasis on maintanability and testability.

A Woma project is composed of these layers:

- Actions: core business logic
- Controllers: map request/response logic to actions
- `Router <woma/router.py>`_: map URLs to endpoints

These layers are conceptual. You are free to organize your code however you
like. Woma makes no assumption about module naming or location.

Basic Usage Example
-------------------

.. code:: python
     
    # -------------------------------------------------------------------------
    # Actions:
    # Your actions should be normal python code that you can use anywhere.
    # They should not depend on the framework.
    # -------------------------------------------------------------------------

    def say_hello(name):
        return 'Hello %s!\n' % name

    # -------------------------------------------------------------------------
    # Controllers:
    # A controller is a way to run your action using data from an http request,
    # and wrap the results in an http response.
    # -------------------------------------------------------------------------

    def hello_controller(request, response):
        name = request.kwargs['name']
        greeting = say_hello(name)
        response.write(greeting)
        return response

    # -------------------------------------------------------------------------
    # Router:
    # The router is a wsgi app that maps paths to other wsgi apps.
    # -------------------------------------------------------------------------

    from woma.router import Router
    router = Router()
    router.map_controllers('/hello/{name}', hello_controller)

To route specific HTTP methods, specify them as kwargs:

.. code:: python

    router.map_controllers('/articles/{article_id}',
        get=show_article, patch=update_article, delete=delete_article)

Deploying
---------

The router is a valid wsgi application. You can serve it however you would
normally serve a wsgi app. Woma doesn't handle this for you.

For example, using uwsgi, you could save the above file as ``app.py`` and run::
    
    $ pip install uwsgi
    $ uwsgi --http :9090 --wsgi-file app.py --callable router &
    $ curl localhost:9090/hello/World
    ...
    'Hello World!'
    $ curl localhost:9090/hello/Justin
    ...
    'Hello Justin!'
    $ kill %1 # assuming uwsgi is background job number 1

Woma Architecture
------------------

Unlike other frameworks, you are not required to inherit from Woma classes to
make the magic happen. As long as your controller conforms to the expected
interface (callable that accepts request and response objects, and returns
the response), you can write your objects however you want.

It shouldn't feel like you are writing a "Woma application". It should feel
like you are writing a python app that uses Woma to deliver it via HTTP.

The controller is your boundary between your app logic and the framework. You
are encouraged to keep this boundary thin by keeping all of your business logic
in actions.

The concept of an "action" in Woma is purely conceptual. There's nothing
stopping you from putting your business logic right in the controller.  But you
are encouraged to break it out into actions that don't depend on the framework.
This will make things easier to test, easier to change, and more resiliant to
changes in the framework.

Status
------

Things are still very very early. Don't use this for anything real yet.

See `the issues <https://github.com/blaix/woma/issues>`_ for an idea of whats
missing and where things are headed.
