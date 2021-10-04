#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2017-2021 MotiveMetrics. All rights reserved.
"""
Spacewalk tools for auto-generating a REST API structure
"""
from marshmallow_jsonschema import JSONSchema

from spacewalk.jobs import NOT_OVERRIDDEN

import logging
log = logging.getLogger(__name__)


class NotLeafError(Exception):
    pass


class Branch():
    """
    A branch node in a Spacewalk tree. Saves the associated job class, REST
    path, and any branches or leaves that are below it.

    A full Spacewalk tree is referenced by its root Branch.

    A Branch job serves as a parent class for the Branches & Leaves below
    it in the tree. It doesn't get run.
    """
    def __init__(self, cls, branches, leaves, path):
        """
        :param cls: job class for this node
        :type cls: :code:`spacewalk.BaseJob` subclass

        :param branches: Branch nodes that are beneath this Branch
        :type branches: list of :code:`spacewalk.BaseJob` subclasses

        :param leaves: Leaf nodes that are beneath this Branch
        :type leaves: list of :code:`spacewalk.BaseJob` subclasses

        :param path: path portion of the Branch's URI
        :type path: str
        """
        self.cls = cls
        self.path = path
        self.branches = {b.cls.BRANCH_NAME: b for b in branches}
        self.leaves = {l.cls.LEAF_NAME: l for l in leaves}


class Leaf():
    """
    An end node in a Spacewalk tree. Saves the associated job class, REST
    path, and the json schema for the job's parameters.

    Leaf jobs are the jobs that actually run.
    """
    def __init__(self, cls, path):
        """
        :param cls: job class for this node
        :type cls: :code:`spacewalk.BaseJob` subclass

        :param path: path portion of the Leaf's URI
        :type path: str
        """
        self.cls = cls
        self.path = path + "/%s" % cls.LEAF_NAME
        self.postschema = JSONSchema().dump(cls.Params())


def auto_tree(rootcls, path):
    """
    Automatically build a Spacewalk tree by recursively walking through the
    subclasses of a root class.

    :param rootcls: the root job class. The Spacewalk tree is built by
        walking through the subclasses of the root.
    :type rootcls: :code:`spacewalk.BaseJob` subclass

    :param path: root path for all the URIs in this tree
    :type path: str

    :returns tree: the :code:`Branch` at the tree's root
    """
    branches = []
    leaves = []

    if is_branch(rootcls):
        path += "/%s" % rootcls.BRANCH_NAME
    else:
        path += "/%s" % rootcls.LEAF_NAME

    for childcls in rootcls.__subclasses__():
        if is_branch(childcls):
            branches.append(auto_tree(childcls, path))
        else:
            leaves.append(Leaf(childcls, path))

    return Branch(rootcls, branches, leaves, path)


def make_path_map(rootbranch, pathmap):
    """
    Recursively build a dictionary that maps all the endpoints in a tree
    to their associated Branches or Leaves

    :param rootbranch: the tree's root :code:`Branch`
    :type rootbranch: :code:`Branch`

    :param pathmap: base pathmap to add to
    :type pathmap: dict

    :returns pathmap:
    """
    pathmap[rootbranch.path] = rootbranch
    for _, leaf in rootbranch.leaves.items():
        pathmap[leaf.path] = leaf

    for _, branch in rootbranch.branches.items():
        pathmap = make_path_map(branch, pathmap)

    return pathmap


def is_branch(cls):
    return len(cls.__subclasses__()) > 0 or cls.LEAF_NAME == NOT_OVERRIDDEN


def targets_by_type(pathmap, targetType):
    return [
        path for path, target in pathmap.items()
        if isinstance(target, targetType)
    ]


class Structure(object):
    """
    Spacewalk structure class which contains a tree and a pathmap, and
    methods to extract useful things from the structure.
    """
    def __init__(self, tree):
        """
        :param tree: root of Spacewalk tree
        :type tree: :code:`Branch`
        """
        self.tree = tree
        self.pathmap = make_path_map(tree, {})

    def get_root_path(self):
        """
        :returns path: root path for this structure
        :rtype: str
        """
        return self.tree.path

    def get_branch_paths(self):
        """
        :returns paths: list of paths to branches
        :rtype: list of str
        """
        return targets_by_type(self.pathmap, Branch)

    def get_leaf_paths(self):
        """
        :returns paths: list of paths to leaves
        :rtype: list of str
        """
        return targets_by_type(self.pathmap, Leaf)

    def get_sub_branches(self, path):
        """
        Return all the sub branches associated with a path.

        :param path: base path
        :type path: str

        :returns sub branches: list of dictionaries for each sub branch.
            Dictionary keys are 'path', 'name', 'description'

        :raises KeyError: if there is no branch for the path
        """
        branch = self.pathmap[path]
        info = []
        for sub in branch.branches.values():
            info.append(
                dict(
                    path=sub.path,
                    name=sub.cls.NAME,
                    description=sub.cls.DESCRIPTION
                )
            )
        return info

    def get_leaves(self, path):
        """
        Return all the leaves associated with a path.

        :param path: base path
        :type path: str

        :returns leaves: list of dictionaries for each leaf
            Dictionary keys are 'path', 'name', 'description'

        :raises KeyError: if there is no branch for the path
        """
        branch = self.pathmap[path]
        info = []
        for leaf in branch.leaves.values():
            info.append(
                dict(
                    path=leaf.path,
                    jobType=leaf.cls.JOB_TYPE,
                    name=leaf.cls.NAME,
                    description=leaf.cls.DESCRIPTION
                )
            )
        return info

    def get_post_schema(self, path):
        """
        get the json-schema for a POST to a leaf

        :param path: path portion of the leaf's URI
        :type path: str

        :returns schema:
        :rtype: json-schema dictionary

        :raises NotLeafError: if path is not for a leaf
        """
        leaf = self.pathmap[path]

        if not isinstance(leaf, Leaf):
            raise NotLeafError

        return leaf.postschema

    def get_job_type(self, path):
        """
        get the job type for a leaf.

        :param path: path portion of the leaf's URI
        :type path: str

        :returns jobType:
        :rtype: str

        :raises NotLeafError: if path is not for a leaf
        """
        leaf = self.pathmap[path]

        if not isinstance(leaf, Leaf):
            raise NotLeafError

        return leaf.cls.JOB_TYPE
