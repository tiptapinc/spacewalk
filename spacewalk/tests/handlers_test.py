import json
import pdb
import pytest

import zerog.registry
from zerog.tests.mock_datastore import MockDatastore
from zerog.tests.mock_queue import MockQueue

from .. import handlers
from .. import server

from . import classes


@pytest.fixture
def app(make_structure):
    """
    Creates a spacewalk app with class structure from 'classes'
    """
    struct = make_structure(classes.Root, "")
    testHandlers = handlers.make_handlers(struct)

    # add some 'bad' handlers to support the bad_branch and not_leaf tests
    testHandlers.append(
        (
            "%s/%s" % ("/whatever", handlers.BRANCHES),
            handlers.SubBranchesHandler
        )
    )
    testHandlers.append(
        (
            "%s/%s" % ("/whatever", handlers.LEAVES),
            handlers.LeavesHandler
        )
    )
    testHandlers.append(
        (
            "%s/%s" % ("/whatever", handlers.POST_SCHEMA),
            handlers.PostSchemaHandler
        )
    )
    testHandlers.append(
        (
            "%s/%s" % ("/whatever", handlers.RUN_JOB),
            handlers.RunJobHandler
        )
    )
    testHandlers.append(
        (
            "%s/%s" % (classes.PROD_PATH, handlers.POST_SCHEMA),
            handlers.PostSchemaHandler
        )
    )
    testHandlers.append(
        (
            "%s/%s" % (classes.PROD_PATH, handlers.RUN_JOB),
            handlers.RunJobHandler
        )
    )
    return server.Server(
        struct,
        MockDatastore(),
        MockQueue(),
        MockQueue(),
        zerog.registry.find_subclasses(classes.Root),
        testHandlers
    )


@pytest.mark.gen_test
def test_sub_branches_handler(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, classes.ROOT_PATH, handlers.BRANCHES)
    )

    assert response.code == 200
    infos = json.loads(response.body)
    assert len(infos) == len(classes.EXPECTED_ROOT_SUB_BRANCH_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_ROOT_SUB_BRANCH_CLASSES:
        assert cls.NAME in names


@pytest.mark.gen_test
def test_leaves_handler(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, classes.EXP_PATH, handlers.LEAVES)
    )

    assert response.code == 200
    infos = json.loads(response.body)
    assert len(infos) == len(classes.EXPECTED_EXP_LEAF_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_EXP_LEAF_CLASSES:
        assert cls.NAME in names


@pytest.mark.gen_test
def test_post_schema_handler(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" %
        (base_url, classes.PARAMS_LEAF_PATH, handlers.POST_SCHEMA)
    )

    assert response.code == 200
    schema = json.loads(response.body)['postSchema']
    assert isinstance(schema, dict)
    assert '$schema' in schema
    assert classes.PARAMS_PROPERTY in (
        schema['definitions']['Params']['properties']
    )


@pytest.mark.gen_test
def test_run_job_handler(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, classes.PARAMS_LEAF_PATH, handlers.RUN_JOB),
        method="POST",
        body=json.dumps({})
    )

    assert response.code == 201
    assert "uuid" in json.loads(response.body)


@pytest.mark.gen_test
def test_sub_branches_bad_path(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, "/whatever", handlers.BRANCHES),
        raise_error=False
    )
    assert response.code == 404


@pytest.mark.gen_test
def test_leaves_bad_path(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, "/whatever", handlers.LEAVES),
        raise_error=False
    )

    assert response.code == 404


@pytest.mark.gen_test
def test_post_schema_bad_path(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, "/whatever", handlers.POST_SCHEMA),
        raise_error=False
    )

    assert response.code == 404


@pytest.mark.gen_test
def test_run_job_bad_path(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, "/whatever", handlers.RUN_JOB),
        method="POST",
        body=json.dumps({}),
        raise_error=False
    )
    assert response.code == 404


@pytest.mark.gen_test
def test_post_schema_not_leaf(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, classes.PROD_PATH, handlers.POST_SCHEMA),
        raise_error=False
    )

    assert response.code == 400


@pytest.mark.gen_test
def test_run_job_not_leaf(app, http_client, base_url):
    response = yield http_client.fetch(
        "%s%s/%s" % (base_url, classes.PROD_PATH, handlers.RUN_JOB),
        method="POST",
        body=json.dumps({}),
        raise_error=False
    )

    assert response.code == 400
