=============================
Sensu client for python
=============================

.. image:: https://badge.fury.io/py/pysensu-ng.svg
    :target: https://badge.fury.io/py/pysensu-ng

.. image:: https://travis-ci.org/sangoma/pysensu.png?branch=master
    :target: https://travis-ci.org/sangoma/pysensu

.. image:: https://pypip.in/d/pysensu-ng/badge.png
    :target: https://pypi.python.org/sangoma/pysensu-ng


This is a client to interact with the Sensu API


Features
--------

- Includes methods for some entrypoints (clients, events, checks, stashes) of the Sensu API (0.24)
  **IMPORTANT**: from 0.6.0 release we are supporting Sensu API 0.24+ .. backward
  compatibility with previous versions of Sensu API might be broken.
- Includes methods for handle subscriptions info (nodes subscribed to a
  specific channel)


Trivial Example
---------------

::

    from pysensu.api import SensuAPI

    url = 'http://localhost:4567'
    my_sensu = SensuAPI(url, username=username, password=password)
    print(my_sensu.get_info())

DEBUG
---------------
To enable debug import logging module and set the debug level

::

    import logging
    logging.getLogger('pysensu.api').setLevel(logging.DEBUG)

Exceptions
---------------
You can handle an exception using a code like this.
Note: Sensu API give you a 404 code if a client does not exists.

::

    import pysensu.api

    url = 'http://localhost:4567'
    my_sensu = pysensu.api.SensuAPI(url)
    client = "testclient"

    try:
        print(my_sensu.get_client_data(client))
    except pysensu.api.SensuAPIException as e:
        if "404" in str(e):
            print("{} does not exists on sensu api".format(client))
        else:
            raise e
