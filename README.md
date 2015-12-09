# Woma

Woma is a collection of python libraries that can be used independently, or
together as a web development framework.

At least that's the plan. It's still in the concept stages. Nothing is even
installable yet.

These pieces exist but are in their infancy:

* [**woma-router**](https://github.com/blaix/woma-router): route requests to wsgi applications
* [**woma-endpoints**](https://github.com/blaix/woma-endpoints): turn callables into wsgi applications

These pieces are planned but are still only a twinkle in my eye:

* **woma-actions**: Callables to perform a unit of work. Composable (e.g. as endpoints, use cases, etc.).
* **woma-validations**: Validate simple data structures.
* **woma-serializers**: Turn objects into simple data structures.
* **woma-repositories**: Persistence for python objects.
* **woma-entities**: High-level package to create objects that can be validated, serialized, and persisted (using the lower-level packages).
* **woma-resources**: High-level package to create RESTful APIs for entities (using the lower-level packages).

It's an experiment in small, decoupled components with a single responsibility,
that can come together in interesting ways to solve larger problems.
