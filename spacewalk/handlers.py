#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2020-2021 MotiveMetrics. All rights reserved.
"""
Request handlers and endpoints for the auto-generated Spacewalk API
"""

import zerog

import json
from tornado.web import HTTPError

from spacewalk.structure import NotLeafError

import logging
log = logging.getLogger(__name__)

UUID_PATT = "(?P<uuid>[^/]*)"           # kwarg == "uuid"

BRANCHES = "branches"
LEAVES = "leaves"
POST_SCHEMA = "post-schema"
RUN_JOB = "job"


class BranchHandler(zerog.BaseHandler):
    """
    Returns a list of sub-branches or leaves for a branch. Must be
    subclassed and subclass must override the :code:`get_collection` method
    """
    def get(self):
        info = self.get_collection()
        self.complete(
            200,
            output=json.dumps(info, indent=4)
        )

    def get_collection(self):
        # subclass this
        pass


class SubBranchesHandler(BranchHandler):
    """
    Returns a list of info dictionaries for each sub-branch of a branch
    """
    def get_collection(self):
        # strip the resource request from the path
        path = self.request.path.replace("/%s" % BRANCHES, "")

        try:
            info = self.application.structure.get_sub_branches(path)
        except KeyError:
            raise HTTPError(404, "No branch for %s" % path)

        return info


class LeavesHandler(BranchHandler):
    """
    Returns a list of info dictionaries for each leaf in a branch
    """
    def get_collection(self):
        # strip the resource request from the path
        path = self.request.path.replace("/%s" % LEAVES, "")

        try:
            info = self.application.structure.get_leaves(path)
        except KeyError:
            raise HTTPError(404, "No branch for %s" % path)

        return info


class PostSchemaHandler(zerog.BaseHandler):
    """
    Returns a JSONSchema of the parameters to pass for a POST to a leaf
    endpoint
    """
    def get(self):
        path = self.request.path.replace("/%s" % POST_SCHEMA, "")

        try:
            schema = self.application.structure.get_post_schema(path)
        except KeyError:
            raise HTTPError(404, "No job for %s" % path)
        except NotLeafError:
            raise HTTPError(400, "%s is a branch, not a job" % path)

        self.complete(
            200,
            output=json.dumps(dict(postSchema=schema), indent=4)
        )


class RunJobHandler(zerog.RunJobHandler):
    """
    Starts a zerog job for a particular endpoint.

    Arguments are validated by attempting to create the job.
    """
    def derive_job_type(self, data, *args, **kwargs):
        path = self.request.path.replace("/%s" % RUN_JOB, "")

        try:
            return self.application.structure.get_job_type(path)
        except KeyError:
            raise HTTPError(404, "No job for %s" % path)
        except NotLeafError:
            raise HTTPError(400, "%s is a branch, not a job" % path)


def make_handlers(structure):
    """
    makes a list of endpoint -> request handler tuples for use by the
    Spacewalk Tornado server
    """
    handlers = []

    # for each branch make endpoints for the SubBranchesHandler and the
    # LeavesHandler
    for path in structure.get_branch_paths():
        handlers.append(("%s/%s" % (path, BRANCHES), SubBranchesHandler))
        handlers.append(("%s/%s" % (path, LEAVES), LeavesHandler))

    # make SchemaHandler and RunJobHandler endpoints for all the leaves
    for path in structure.get_leaf_paths():
        handlers.append(("%s/%s" % (path, POST_SCHEMA), PostSchemaHandler))
        handlers.append(("%s/%s" % (path, RUN_JOB), RunJobHandler))

    handlers += [
        (
            "%s/progress/%s" % (structure.get_root_path(), UUID_PATT),
            zerog.ProgressHandler
        ), (
            "%s/info/%s" % (structure.get_root_path(), UUID_PATT),
            zerog.InfoHandler
        ), (
            "%s/data/%s" % (structure.get_root_path(), UUID_PATT),
            zerog.GetDataHandler
        ), (
            "%s/dump/%s" % (structure.get_root_path(), UUID_PATT),
            zerog.DumpHandler
        )
    ]

    return handlers
