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
    must override:
        NAME
        BRANCH_NAME (if branch) or LEAF_NAME (if leaf)
        DESCRIPTION

    may override:
        BASE_SCHEMA
        Params
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
        super(BaseJob, self).__init__(*args, **kwargs)

        # add Params to job
        for key in self.Params().fields.keys():
            if key in kwargs:
                setattr(self, key, kwargs[key])
