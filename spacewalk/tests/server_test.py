import pdb
import pytest

from zerog.tests.mock_datastore import MockDatastore
from zerog.tests.mock_queue import MockQueue

from ..server import Server
from . import classes


def test_server_init(make_structure):
    struct = make_structure(classes.Root, "")
    Server(
        struct,
        MockDatastore(),
        MockQueue(),
        MockQueue(),
        []
    )

    assert True
