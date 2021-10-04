.. Spacewalk documentation master file, created by
   sphinx-quickstart on Tue Sep 28 11:35:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Spacewalk
=========
Spacewalk is an add-on to the `ZeroG`_ job-processing system that auto-generates a discoverable, self-documenting REST API for a set of ZeroG job classes. Pass Spacewalk a modules directory and a base job class derived from ``spacewalk.BaseJob``, and Spacewalk will create a REST API with endpoints for all subclasses of the base job that it finds.

.. _Zerog: https://github.com/tiptapinc/zerog

ZeroG Documentation
===================
To understand Spacewalk, it helps to first review the ZeroG job-processing system on which it is based. ZeroG documentation can be found at:

- ZeroG: https://zerog.readthedocs.io/en/latest/

Install Spacewalk
=================
.. code-block:: console

    $ pip install -e git+https://github.com/tiptapinc/spacewalk.git@0.0.5#egg=spacewalk

Spacewalk Documentation
=======================
.. toctree::
   :maxdepth: 2
   :caption: Examples & Reference:

   api_example
   code_examples
   run_examples
   api_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
