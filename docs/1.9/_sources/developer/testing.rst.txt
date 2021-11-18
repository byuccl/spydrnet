Testing
=======

SpyDrNet developers strive to provide high quality code that is well tested. To help accomplish this goal, the built-in Python `Unit testing framework <https://docs.python.org/3/library/unittest.html>`__ is used in conjunction with the ``pytest`` `package <https://docs.pytest.org/>`__.

Running Tests
-------------

There are many ways to execute the suite of tests that have been developed for SpyDrNet. SpyDrNet source code can be tested by executing the following command from within the directory of the repository::

    pytest spydrnet
    
If SpyDrNet has been installed (as a release or in developer mode) the tests can run using the following command::

   pytest --pyargs spydrnet

If SpyDrNet can be imported, then its tests can be run::

    >>> import spydrnet as sdn
    >>> sdn.test()

.. autofunction:: spydrnet.test

Code Coverage
-------------

Optionally, test code coverage information can be collected using the ``pytest-cov`` `package <https://pytest-cov.readthedocs.io/>`_ and the ``--cov`` pytest flag::

    > pytest --cov <additional arguments>
    
The ``pytest-cov`` package must be installed to generate this report::

    > pip install pytest-cov
    
The report can be limited to a subset of code by adding a module path to the ``--cov`` flag::

    > pytest --cov=spydrnet.<dot path to specific module or package>
    
The coverage report can be extended to included the terms missing from the test by setting the ``--cov-report`` flag::

    > pytest --cov --cov-report=term-missing
    
Generally, 100% code coverage is desired. Listing any terms missing greatly assists in the construction of additional tests.
