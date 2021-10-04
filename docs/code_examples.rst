Code Examples
=============
Make a Job Hierarchy
----------------------

.. code-block:: python

    from marshmallow import fields, Schema
    import random
    import spacewalk
    import time


    class BaseExampleJobSchema(spacewalk.BaseJobSchema):
        pass


    class BaseExampleJob(spacewalk.BaseJob):
        NAME = "Spacewalk Example"
        BRANCH_NAME = "examples"
        DESCRIPTION = "example Spacewalk jobs"

        BASE_SCHEMA = BaseExampleJobSchema

        def run(self):
            self.job_log_info(f"starting {self.jobType} job {self.uuid}")


    class WasteTimeJob(BaseExampleJob):
        NAME = "Waste Time Job"
        LEAF_NAME = "waste_time"
        DESCRIPTION = "Randomly logs while wasting time"

        class Params(Schema):
            delay = fields.Integer()

        def run(self):
            super().run()

            end = time.time() + self.delay
            logInterval = self.delay / 10

            while True:
                if time.time() > end:
                    break

                logDelay = (random.random() + 0.5) * logInterval
                time.sleep(logDelay)
                self.add_to_completeness(logDelay / self.delay)
                self.job_log_info(f"{end - time.time():.2f} seconds remaining")

            return 200, None


    class FizzBuzzJobSchema(BaseExampleJobSchema):
        output = fields.List(fields.String)


    class FizzBuzzJob(BaseExampleJob):
        NAME = "FizzBuzz Job"
        LEAF_NAME = "fizz_buzz"
        DESCRIPTION = "Solve FizzBuzz with settable n, fizz & buzz divisors"

        BASE_SCHEMA = FizzBuzzJobSchema

        class Params(Schema):
            n = fields.Integer(default=50, missing=50)
            fizzDivisor = fields.Integer(default=3, missing=3)
            buzzDivisor = fields.Integer(default=5, missing=5)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.output = kwargs.get("output", [])

        def run(self):
            super().run()

            divisors = [self.fizzDivisor, self.buzzDivisor]
            output = []

            for i in range(1, self.n + 1):
                remainders = list(map(lambda x: i % x, divisors))
                if remainders == [0, 0]:
                    msg = "FizzBuzz"
                elif remainders[0] == 0:
                    msg = "Fizz"
                elif remainders[1] == 0:
                    msg = "Buzz"
                else:
                    msg = str(i)

                output.append(msg)

            self.update_attrs(output=output)
            return 200, None

Create & Start a Spacewalk Service
------------------------------------

.. code-block:: python

    import spacewalk
    import tornado.ioloop
    import zerog


    def make_datastore():
        return zerog.CouchbaseDatastore(
            "couchbase", "Administrator", "password", "test"
        )


    def make_queue(queueName):
        return zerog.BeanstalkdQueue("beanstalkd", 11300, queueName)


    def start_server():
        tree = spacewalk.auto_tree(BaseExampleJob, "")
        struct = spacewalk.Structure(tree)
        handlers = spacewalk.make_handlers(struct)

        server = spacewalk.Server(
            struct,
            "myService",
            make_datastore,
            make_queue,
            [WasteTimeJob, FizzBuzzJob],
            handlers
        )
        server.listen(8888)
        tornado.ioloop.IOLoop.current().start()


    start_server()
