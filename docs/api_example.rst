Auto-Generated API
==================

Spacewalk generates a fully discoverable and self-documenting REST API for initiating, monitoring, and querying ZeroG jobs.

Branches
--------
Query the base endpoint to get available branches in the endpoint hierarchy:

.. code-block:: console

    $ curl spacewalk:8888/examples/branches

    []

Leaves
------
Query a branch to get the available jobs:

.. code-block:: console

    $ curl spacewalk:8888/examples/leaves

    [
        {
            "path": "/examples/waste_time",
            "jobType": "examples_waste_time",
            "name": "Waste Time Job",
            "description": "Randomly logs while wasting time"
        },
        {
            "path": "/examples/fizz_buzz",
            "jobType": "examples_fizz_buzz",
            "name": "FizzBuzz Job",
            "description": "Solve FizzBuzz with settable n, fizz & buzz divisors"
        }
    ]

Schemas
-------
Query an individual job to get its input parameters in JSON-Schema form:

.. code-block:: console

    $ curl spacewalk:8888/examples/fizz_buzz/post-schema

    {
        "postSchema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "definitions": {
                "Params": {
                    "properties": {
                        "buzzDivisor": {
                            "title": "buzzDivisor",
                            "type": "number",
                            "format": "integer",
                            "default": 5
                        },
                        "fizzDivisor": {
                            "title": "fizzDivisor",
                            "type": "number",
                            "format": "integer",
                            "default": 3
                        },
                        "n": {
                            "title": "n",
                            "type": "number",
                            "format": "integer",
                            "default": 50
                        }
                    },
                    "type": "object",
                    "additionalProperties": false
                }
            },
            "$ref": "#/definitions/Params"
        }
    }

Run a Job
---------
Use an HTTP POST to initiate a job:

.. code-block:: console

    $ curl -X POST -H 'Content-Type: application/json' -d '{"n":20}' spacewalk:8888/examples/fizz_buzz/job

    {
        "uuid": "d5de4383-ea62-47a0-85fd-419762c457c6"
    }

Monitor a Job
-------------
Monitor the job's progress:

.. code-block:: console

    $ curl spacewalk:8888/examples/progress/d5de4383-ea62-47a0-85fd-419762c457c6

    {
        "completeness": 1.0,
        "result": 200
    }

Job Details
-----------
Get full details of the job's run:

.. code-block:: console

    $ curl spacewalk:8888/examples/info/d5de4383-ea62-47a0-85fd-419762c457c6

    {
        "completeness": 1.0,
        "result": 200,
        "events": [
            {
                "msg": "starting examples_fizz_buzz job d5de4383-ea62-47a0-85fd-419762c457c6",
                "timeStamp": "2021-09-28T14:51:57.209432"
            }
        ],
        "errors": [],
        "warnings": []
    }

Job Results
-----------
Get the job's results:

.. code-block:: console

    $ curl spacewalk:8888/examples/data/d5de4383-ea62-47a0-85fd-419762c457c6

    {
        "output": [
            "1",
            "2",
            "Fizz",
            "4",
            "Buzz",
            "Fizz",
            "7",
            "8",
            "Fizz",
            "Buzz",
            "11",
            "Fizz",
            "13",
            "14",
            "FizzBuzz",
            "16",
            "17",
            "Fizz",
            "19",
            "Buzz"
        ]
    }
