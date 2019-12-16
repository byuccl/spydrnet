Introduction
============

GitHub Repository
-----------------

The offical SpyDrNet repository resides at https://github.com/byuccl/spydrnet/. Code in the master branch is the latest
production code. It should be tested, documented, and include examples of use. All modifications to the master branch
are recieved through pull requests (either forks, or branches within the project itself). For help getting started with
GitHub and git, see `GitHub Guides <https://guides.github.com/>`_.

Testing
-------

Testing is implemented using the built-in `unit testing framework <https://docs.python.org/3.5/library/unittest.html>`_
and `pytest <https://docs.pytest.org/en/latest/>`_. The pytest package must be installed to run the tests using pytest.

**Running All Tests**

Tests can be run form an interactive console::

    >>> import spydrnet as sdn
    >>> sdn.test()
    
Or, if SpyDrNet is installed (either as a package or in editable mode - see `README.rst`), tests can be run from the
command line in the project directory as follows::

    > pytest spydrnet
    
**Checking Test Coverage**

Test coverage is checked using `pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`_ - a pytest plug-in for code 
coverage analysis. The pytest-cov package must be installed to run this report. Code coverage analysis can be run as 
follows::

    > pytest spydrnet --cov=spydrnet
    
To report missing terms (not covered by any test), use the following command::

    > pytest spydrnet --cov=spydrnet<.any_specific_submodule> --cov-report=term-missing 