from marshmallow import Schema, fields
import time

from spacewalk.jobs import BaseJob


class Root(BaseJob):
    NAME = "root"
    BRANCH_NAME = "root"
    DESCRIPTION = "root of the whole thang"


class ProdBranch(Root):
    NAME = "prod"
    BRANCH_NAME = "prod"
    DESCRIPTION = "production jobs"


class DevBranch(Root):
    NAME = "dev"
    BRANCH_NAME = "dev"
    DESCRIPTION = "dev jobs"


class DevExpBranch(DevBranch):
    NAME = "experimental"
    BRANCH_NAME = "exp"
    DESCRIPTION = "experimental stuff that might break"


class ProdLeaf1(ProdBranch):
    NAME = "useful production job"
    LEAF_NAME = "useful"
    DESCRIPTION = "job that does useful stuff"

    class Params(Schema):
        thingum = fields.String()

    def run(self):
        return 200, None


class ProdLeaf2(ProdBranch):
    NAME = "also useful"
    LEAF_NAME = "also-useful"
    DESCRIPTION = "job that is also useful"


class ProdLeaf3(ProdBranch):
    NAME = "super useful"
    LEAF_NAME = "super-useful"
    DESCRIPTION = "job that is super-duper useful"


class DevLeaf1(DevBranch):
    NAME = "fake run"
    LEAF_NAME = "fake-run"
    DESCRIPTION = "job that pretends to run & updates completeness"

    # worker doesn't seem to be running in the test environment -- need
    # to figure that out
    def run(self):
        time.sleep(1)
        self.add_to_completeness(.5)
        time.sleep(1)
        return 200, None


class DevLeaf2(DevBranch):
    NAME = "needs testing"
    LEAF_NAME = "needs-testing"
    DESCRIPTION = "job that needs more testing"


class ExpLeaf1(DevExpBranch):
    NAME = "new thing"
    LEAF_NAME = "new-thing"
    DESCRIPTION = "some new thing we're just inventing"


class ExpLeaf2(DevExpBranch):
    NAME = "crazy"
    LEAF_NAME = "crazy"
    DESCRIPTION = "crazy job that probably won't work"


class EmptyBranch(ProdBranch):
    NAME = "empty branch"
    BRANCH_NAME = "empty-branch"
    DESCRIPTION = "branch with no leaves in it"


BRANCH_CLASSES = [Root, ProdBranch, DevBranch, DevExpBranch, EmptyBranch]
LEAF_CLASSES = [
    ProdLeaf1, ProdLeaf2, ProdLeaf3, DevLeaf1, DevLeaf2, ExpLeaf1, ExpLeaf2
]

EXPECTED_ROOT_BRANCH_COUNT = 2
EXPECTED_ROOT_LEAF_COUNT = 0

EXPECTED_MAPPINGS = {
    "/root": Root,
    "/root/prod": ProdBranch,
    "/root/dev": DevBranch,
    "/root/dev/exp": DevExpBranch,
    "/root/prod/useful": ProdLeaf1,
    "/root/prod/also-useful": ProdLeaf2,
    "/root/prod/super-useful": ProdLeaf3,
    "/root/dev/fake-run": DevLeaf1,
    "/root/dev/needs-testing": DevLeaf2,
    "/root/dev/exp/new-thing": ExpLeaf1,
    "/root/dev/exp/crazy": ExpLeaf2,
    "/root/prod/empty-branch": EmptyBranch
}

EXPECTED_BRANCH_PATHS = [
    path for path, cls in EXPECTED_MAPPINGS.items()
    if cls in BRANCH_CLASSES
]

EXPECTED_LEAF_PATHS = [
    path for path, cls in EXPECTED_MAPPINGS.items()
    if cls in LEAF_CLASSES
]

ROOT_PATH = "/root"
PROD_PATH = "/root/prod"
DEV_PATH = "/root/dev"
EXP_PATH = "/root/dev/exp"

DEV_LEAF_PATH = "/root/dev/needs-testing"
EXP_LEAF_PATH = "/root/dev/exp/crazy"

PARAMS_LEAF_PATH = "/root/prod/useful"
PARAMS_PROPERTY = "thingum"

JOB_THAT_RUNS = DevLeaf1
JOB_THAT_RUNS_PATH = "/root/dev/fake-run"

EXPECTED_ROOT_SUB_BRANCH_CLASSES = [ProdBranch, DevBranch]
EXPECTED_PROD_LEAF_CLASSES = [ProdLeaf1, ProdLeaf2, ProdLeaf3]
EXPECTED_DEV_SUB_BRANCH_CLASSES = [DevExpBranch]
EXPECTED_EXP_LEAF_CLASSES = [ExpLeaf1, ExpLeaf2]
