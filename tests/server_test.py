import pdb
import pytest
import zerog

import spacewalk
from . import classes


def test_server_init(make_structure, make_datastore, make_queue):
    struct = make_structure(classes.Root, "")

    spacewalk.Server(
        struct,
        "testService",
        make_datastore,
        make_queue,
        zerog.registry.find_subclasses(classes.Root),
        []
    )
    assert True
