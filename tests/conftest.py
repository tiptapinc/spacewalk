import pdb
import pytest

from spacewalk import structure


@pytest.fixture
def make_structure():
    def func(rootcls, basepath):
        tree = structure.auto_tree(rootcls, basepath)
        return structure.Structure(tree)

    return func
