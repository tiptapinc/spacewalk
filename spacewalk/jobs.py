#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2020-2021 MotiveMetrics. All rights reserved.
"""
BaseJob and BaseJobSchema for building out a Spacewalk job processing
service
"""

from marshmallow import Schema
import zerog

import logging
log = logging.getLogger(__name__)

NOT_OVERRIDDEN = "spacewalk-base"


def job_type(branch, leaf):
    return "%s_%s" % (branch, leaf)


def schema_name(branch, leaf):
    return "%s%sSchema" % (branch.capitalize(), leaf.capitalize())


class BaseJobSchema(zerog.BaseJobSchema):
    pass


class BaseJob(zerog.BaseJob):
    """
    The base class for all Spacewalk jobs.

    :cvar str NAME: Human friendly job or branch name which will be shown
        for the /branches or /leaves endpoint. You MUST override this attribute
        for all jobs.

    :cvar str BRANCH_NAME: Name by which a branch is identified in endpoints.
        You MUST override this attribute for a branch (parent) job

    :cvar str LEAF_NAME: Name by which a leaf is identified in endpoints.
        You MUST override this attribute for a leaf (endpoint) job

    :cvar str DESCRIPTION: Human friendly string describing the job in more
        detail. This description will be shown in the /branches or /leaves
        endpoint. You MUST override this attribute for all jobs.

    :cvar class BASE_SCHEMA: The marshmallow schema used to
        serialize/deserialize this job. You MAY override this attribute to
        add fields to the base schema. The schema MUST be a subclass of
        BaseJobSchema.

    :cvar class Params: The marshmallow schema used to define this job's
        input parameters for an HTTP POST to the /job endpoint, which creates
        a job. You MAY override this attribute to define your job's inputs.
        The /post-schema endpoint will document these input Params as a
        JSON-Schema. The Params class definition can be nested in the job
        class as shown here, or defined outside the job class and assigned
        as a class attribute.

    Subclasses MUST

        - override the ``run()`` method
    """
    NAME = NOT_OVERRIDDEN
    BRANCH_NAME = NOT_OVERRIDDEN
    LEAF_NAME = NOT_OVERRIDDEN
    DESCRIPTION = NOT_OVERRIDDEN

    BASE_SCHEMA = BaseJobSchema

    class Params(Schema):
        # Override this to define subclass-unique parameters
        pass

    @classmethod
    def __init_subclass__(cls, **kwargs):
        # auto-override the zerog.BaseJob properties SCHEMA and JOB_TYPE
        # for all Spacewalk subclasses. This method is called when any of
        # this class's subclasses are imported.
        #
        #   Args:
        #       cls: The subclass being imported
        #
        # JOB_TYPE is composed by combining this class's RESOURCE
        cls.JOB_TYPE = job_type(cls.BRANCH_NAME, cls.LEAF_NAME)

        # SCHEMA inherits from BASE_SCHEMA and Params
        cls.SCHEMA = type(
            schema_name(cls.BRANCH_NAME, cls.LEAF_NAME),
            (cls.BASE_SCHEMA, cls.Params),
            {}
        )

        # have to run the parent's __init_subclass__ AFTER overriding
        # JOB_TYPE and SCHEMA.
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """
        Initialize the job with deserialized data.

        Subclasses MUST override this method if they use a subclass of
        BaseJobSchema to add fields.

        If overriding this method, you MUST call the parent ``__init__()``
        using ``super``

        This ``__init__()`` method is the opportunity to load any extra
        fields that are declared in the associated schema.

        Required fields can be loaded directly by referencing their key.

        Optional fields need to be loaded using the dictionary's ``get``
        method, which gives an opportunity to load the field with a default
        value if it isn't present in the input data.

        Example::

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.requiredField = kwargs['requiredField']
                self.optionalField = kwargs.get('optionalField', "default")
        """
        super(BaseJob, self).__init__(*args, **kwargs)

        # add Params to job
        for key in self.Params().fields.keys():
            if key in kwargs:
                setattr(self, key, kwargs[key])
