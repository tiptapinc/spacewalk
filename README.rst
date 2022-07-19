*********
Spacewalk
*********

Introduction
============

Spacewalk is an add-on to the `ZeroG`_ job-processing system that auto-generates a discoverable, self-documenting REST API for a set of ZeroG job classes. Pass Spacewalk a modules directory and a base job class derived from ``spacewalk.BaseJob``, and Spacewalk will create a REST API with endpoints for all subclasses of the base job that it finds.

.. _Zerog: https://github.com/tiptapinc/zerog

Install Spacewalk
=================

.. code-block:: console

    $ pip install -e git+https://github.com/tiptapinc/spacewalk.git@0.0.5#egg=spacewalk

Documentation
=============

- ZeroG: https://zerog.readthedocs.io/en/latest/
- Spacewalk: https://zerog-spacewalk.readthedocs.io/en/latest

Auto-Generated API
==================

Spacewalk generates a fully discoverable and self-documenting REST API for initiating, monitoring, and querying ZeroG jobs.

Query the base endpoint to get available branches in the endpoint hierarchy:

.. code-block:: console

    $ curl spacewalk:8888/examples/branches

    []

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

Use an HTTP POST to initiate a job:

.. code-block:: console

    $ curl -X POST -H 'Content-Type: application/json' -d '{"n":20}' spacewalk:8888/examples/fizz_buzz/job

    {
        "uuid": "d5de4383-ea62-47a0-85fd-419762c457c6"
    }

Monitor the job's progress:

.. code-block:: console

    $ curl spacewalk:8888/examples/progress/d5de4383-ea62-47a0-85fd-419762c457c6

    {
        "completeness": 1.0,
        "result": 200
    }

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

Get a full dump of the job (showLogs parameter inludes or excludes logs, false by default):

.. code-block:: console

    $ curl spacewalk:8888/examples/dump/9726b1fa-01e0-4c10-931e-55128415587d?showLogs=true

    {
        "documentType": "zerog_job",
        "datasetName": "bids",
        "endDate": null,
        "createdAt": "2021-11-20T02:55:10.967790",
        "logId": "gaql_load-dataset_9726b1fa-01e0-4c10-931e-55128415587d",
        "startDate": null,
        "queueKwargs": {
            "ttr": 2592000
        },
        "updatedAt": "2021-11-20T02:55:25.709894",
        "name": "Boots Report",
        "schemaVersion": 1.0,
        "running": false,
        "uuid": "9726b1fa-01e0-4c10-931e-55128415587d",
        "queueJobId": 4,
        "customerId": "2464420064",
        "errorCount": 0,
        "jobType": "gaql_load-dataset",
        "tickcount": 1.0,
        "completeness": 1.0,
        "resultCode": 200,
        "cas": 1637376925711663104,
        "tickval": 1.0,
        "action": "load"
}
