#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2017-2021 MotiveMetrics. All rights reserved.
"""
Spacewalk Server class definition
"""
import zerog


class Server(zerog.Server):
    """
    Base Spacewalk server class
    """
    def __init__(self, structure, *args, **kwargs):
        """
        :param structure: object that defines the tree and pathmap for
            an auto-generated spacewalk REST API
        :type structure: spacewalk.Structure

        :param `*args`: positional arguments passed through to the
            ``zerog.Server`` parent class

        :param `**kwargs`: keyword arguments passed through to the
            ``zerog.Server`` parent class
        """
        super(Server, self).__init__(*args, **kwargs)

        self.structure = structure
