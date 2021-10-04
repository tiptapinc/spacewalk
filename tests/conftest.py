import pdb
import pytest
import zerog

from spacewalk import structure


@pytest.fixture
def make_structure():
    def func(rootcls, basepath):
        tree = structure.auto_tree(rootcls, basepath)
        return structure.Structure(tree)

    return func


@pytest.fixture
def datastore():
    return zerog.CouchbaseDatastore(
        "couchbase", "Administrator", "password", "test"
    )


@pytest.fixture
def make_datastore(datastore):
    def _func():
        return datastore

    return _func


@pytest.fixture
def make_queue():
    """
    creates a beanstalkd queue object

    assumes a docker-compose environment with beanstalkd container at
    hostname "beanstalkd"
    """
    def _func(queueName):
        return zerog.BeanstalkdQueue("beanstalkd", 11300, queueName)

    return _func
