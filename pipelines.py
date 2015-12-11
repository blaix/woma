from copy import deepcopy
from functools import reduce
from uuid import uuid4
import json

def deserialize(input):
    return json.loads(input)

def set_defaults(input):
    output = deepcopy(input)
    output.setdefault('id', uuid4().hex)
    return output

def validate(input):
    if 'name' not in input:
        raise Exception('name is required')
    return input

class P(object):
    def __init__(self, *pipeline):
        self.pipeline = pipeline

    def __add__(self, *pipeline):
        return P(*(self.pipeline + pipeline))

    def __call__(self, data):
        reducer = lambda data, func: func(data)
        return reduce(reducer, self.pipeline, data)

clean = P(deserialize, set_defaults, validate)

RECORDS = []
clean_and_persist = clean + RECORDS.append

clean_and_persist('{"name": "Justin"}')
print("Records are: %s " % RECORDS)

try:
    clean_and_persist('{"foo": "bar"}')
except Exception as e:
    print("Failed with %s" % e)
print("Records are: %s " % RECORDS)

"""Thoughts:
    * make explicit which funcs are not pure (e.g. persist)?
        * pass through the previous input instead of requiring return?
    * enforce immutability of input? (how? always deepcopy data in reducer?)
    * best way to handle failures? (exceptions? L/R monads?)
"""

# Possible example of what a pipeline-based endpoint might look like:

@endpoint
class ResourceEndpoint(object):
    def __init__(repo, validator=None):
        self.repo = repo
        self.validator = validator or lambda input: input

    def post(self, req: Request):
        return self._create_resource(req.POST)

    @property
    def _create_resource(self):
        return P(json.loads,
                validate_article,
                article_repository.insert,
                json.dumps)

article_endpoint = ResourceEndpoint(repo=ArticleRepo())
router.add('/articles', article_endpoint)
