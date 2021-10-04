Run Examples in Docker
======================

Install Docker
--------------
`Install Docker`_

.. _Install Docker: https://docs.docker.com/get-docker/

Clone Spacewalk Repository
--------------------------

.. code-block:: console

	$ git clone https://github.com/tiptapinc/spacewalk.git

Run With Docker-Compose
-----------------------

.. code-block:: console

	$ docker-compose up --build

Docker Exec to Spacewalk Container
----------------------------------
.. code-block:: console

	$ docker exec -it spacewalk_spacewalk_1 bash
