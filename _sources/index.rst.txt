unityapiclient
==============

This is a client library for the `Unity IDM <http://www.unity-idm.eu/>`_ APIs.

Currently, it only supprorts a subset of the operations exposed by Unity's Administration API.

Python version
--------------

Python 2.6 or 2.7 are fully supported.

Installation
------------

To install the client library, simply run:

.. code-block:: bash

    $ pip install unityapiclient
    🍺

Third party libraries and dependencies
--------------------------------------

The following libraries will be installed when you install the client library:

* `pytz <https://github.com/newvem/pytz>`_
* `requests <https://github.com/kennethreitz/requests>`_

Usage
-----

The following example assumes a Unity IDM deployment at ``https://unity.example.org``:

.. code-block:: python

    >>> import unityapiclient
    >>> from unityapiclient.client import UnityApiClient
    >>> client = UnityApiClient('https://unity.example.org',
    ... auth=('unityapiuser', 'secretpassword'))
    >>> entity = client.get_entity(257)
    >>> entity['entityInformation']['state']
    u'valid'

Reference  
=========

.. toctree::
   :maxdepth: 2

   client

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
