from marshmallow import Schema
import zerog

import logging
log = logging.getLogger(__name__)


def job_type(bench, endpoint):
    return "lab_%s_%s" % (bench, endpoint)


def schema_name(bench, endpoint):
    return "%s%sSchema" % (bench.capitalize(), endpoint.capitalize())


class BaseJobSchema(zerog.BaseJobSchema):
    pass


class BaseJob(zerog.BaseJob):
    """
    must override:
        NAME
        BRANCH_NAME or LEAF_NAME
        DESCRIPTION

    may override:
        BASE_SCHEMA
        Params
    """
    NAME = "short name"
    BRANCH_NAME = "name-of-branch-for-url"
    LEAF_NAME = "name-of-leaf-for-url"
    DESCRIPTION = "long description"

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
        log.info("calling lab job with args:%s, kwargs:%s" % (args, kwargs))
        super(BaseJob, self).__init__(*args, **kwargs)

        # add Params to job
        for key in self.Params().fields.keys():
            setattr(self, key, kwargs.get(key))
