#!/usr/bin/env python
# encoding: utf-8
"""
Copyright (c) 2020 MotiveMetrics. All rights reserved.

"""
from marshmallow_jsonschema import JSONSchema

from spacewalk.jobs import NOT_OVERRIDDEN

import logging
log = logging.getLogger(__name__)


class NotLeafError(Exception):
    pass


class Branch():
    def __init__(self, cls, branches, leaves, path):
        self.cls = cls
        self.path = path
        self.branches = {b.cls.BRANCH_NAME: b for b in branches}
        self.leaves = {l.cls.LEAF_NAME: l for l in leaves}


class Leaf():
    def __init__(self, cls, path):
        self.cls = cls
        self.path = path + "/%s" % cls.LEAF_NAME
        self.postschema = JSONSchema().dump(cls.Params())


def auto_tree(rootcls, path):
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
    def __init__(self, tree):
        self.tree = tree
        self.pathmap = make_path_map(tree, {})

    def get_root_path(self):
        return self.tree.path

    def get_branch_paths(self):
        return targets_by_type(self.pathmap, Branch)

    def get_leaf_paths(self):
        return targets_by_type(self.pathmap, Leaf)

    def get_sub_branches(self, path):
        """
        Return all the sub branches associated with a path.

        Args:
            path: path portion of a uri

        Returns:
            list of dictionaries for each sub branch.
            Dictionary keys are 'path', 'name', 'description'

        Raises KeyError if there is no branch for the path
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

        Args:
            path: path portion of a uri

        Returns:
            list of dictionaries for each leaf.
            Dictionary keys are 'path', 'name', 'description'

        Raises KeyError if there is no branch for the path
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
        leaf = self.pathmap[path]

        if not isinstance(leaf, Leaf):
            raise NotLeafError

        return leaf.postschema

    def get_job_type(self, path):
        """
        Returns the job type for a leaf.
        """
        leaf = self.pathmap[path]

        if not isinstance(leaf, Leaf):
            raise NotLeafError

        return leaf.cls.JOB_TYPE
