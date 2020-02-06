import pdb
import pytest

from .. import structure
from . import classes


def test_make_branch():
    b = structure.Branch(
        classes.Root,
        [],
        [],
        "/tests"
    )

    assert b.cls == classes.Root
    assert b.path == "/tests"
    assert len(b.branches) == 0
    assert len(b.leaves) == 0


def test_make_leaf():
    l = structure.Leaf(classes.ProdLeaf1, "/tests")

    assert l.cls == classes.ProdLeaf1
    assert l.path == "/tests/%s" % classes.ProdLeaf1.LEAF_NAME


def test_make_tree():
    tree = structure.make_tree(classes.Root, "/tests")

    assert isinstance(tree, structure.Branch)
    assert tree.cls == classes.Root
    assert tree.path == "/tests/%s" % classes.Root.BRANCH_NAME
    assert len(tree.branches) == classes.EXPECTED_ROOT_BRANCH_COUNT
    assert len(tree.leaves) == classes.EXPECTED_ROOT_LEAF_COUNT


def test_initialize_structure():
    tree = structure.make_tree(classes.Root, "/tests")
    structure.Structure(tree)

    assert True


def test_branch_paths(make_structure):
    struct = make_structure(classes.Root, "")
    paths = struct.get_branch_paths()

    assert len(set(paths) - set(classes.EXPECTED_BRANCH_PATHS)) == 0
    assert len(set(classes.EXPECTED_BRANCH_PATHS) - set(paths)) == 0


def test_leaf_paths(make_structure):
    struct = make_structure(classes.Root, "")
    paths = struct.get_leaf_paths()

    assert(len(set(paths) - set(classes.EXPECTED_LEAF_PATHS))) == 0
    assert(len(set(classes.EXPECTED_LEAF_PATHS) - set(paths))) == 0


def test_get_root_sub_branches(make_structure):
    struct = make_structure(classes.Root, "")
    infos = struct.get_sub_branches(classes.ROOT_PATH)

    assert len(infos) == len(classes.EXPECTED_ROOT_SUB_BRANCH_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_ROOT_SUB_BRANCH_CLASSES:
        assert cls.NAME in names


def test_get_dev_sub_branches(make_structure):
    struct = make_structure(classes.Root, "")
    infos = struct.get_sub_branches(classes.DEV_PATH)

    assert len(infos) == len(classes.EXPECTED_DEV_SUB_BRANCH_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_DEV_SUB_BRANCH_CLASSES:
        assert cls.NAME in names


def test_get_prod_leaves(make_structure):
    struct = make_structure(classes.Root, "")
    infos = struct.get_leaves(classes.PROD_PATH)

    assert len(infos) == len(classes.EXPECTED_PROD_LEAF_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_PROD_LEAF_CLASSES:
        assert cls.NAME in names


def test_get_exp_leaves(make_structure):
    struct = make_structure(classes.Root, "")
    infos = struct.get_leaves(classes.EXP_PATH)

    assert len(infos) == len(classes.EXPECTED_EXP_LEAF_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_EXP_LEAF_CLASSES:
        assert cls.NAME in names


def test_get_dev_post_schema(make_structure):
    struct = make_structure(classes.Root, "")
    schema = struct.get_post_schema(classes.DEV_LEAF_PATH)

    assert isinstance(schema, dict)
    assert '$schema' in schema
    assert 'definitions' in schema


def test_get_post_schema_with_params(make_structure):
    struct = make_structure(classes.Root, "")
    schema = struct.get_post_schema(classes.PARAMS_LEAF_PATH)

    assert isinstance(schema, dict)
    assert '$schema' in schema
    assert classes.PARAMS_PROPERTY in (
        schema['definitions']['Params']['properties']
    )


def test_non_empty_base_path(make_structure):
    basepath = "/test/base/path"
    struct = make_structure(classes.Root, basepath)
    infos = struct.get_leaves("%s%s" % (basepath, classes.PROD_PATH))

    assert len(infos) == len(classes.EXPECTED_PROD_LEAF_CLASSES)
    assert isinstance(infos[0], dict)
    assert "path" in infos[0]
    assert "name" in infos[0]
    assert "description" in infos[0]

    names = [info['name'] for info in infos]
    for cls in classes.EXPECTED_PROD_LEAF_CLASSES:
        assert cls.NAME in names
