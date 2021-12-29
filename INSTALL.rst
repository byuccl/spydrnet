.. _INSTALL.rst:

Install
=======

SpyDrNet requires Python 3.6 or newer. Please ensure that this prerequisite has been met before proceeding.

This guide shows how to install SpyDrNet in the default Python environment (from the `Python website <https://python.org>`_). If a different environment is used, adapt these instructions as necessary. For all ``pip`` installations, make sure ``pip`` is up-to-date by executing the following command::

    > python -m pip install --upgrade pip
    
More instruction on installing ``pip`` (the Python package manager) is provided in the `PIP installation documentation <https://pip.pypa.io/en/stable/installing>`_.

Install a Release
-----------------

The stable release of SpyDrNet can be installed using ``pip``::

    > pip install spydrnet
    
It can be installed using the ``--user`` to avoid permission issues::

    > pip install --user spydrnet
    
It can be to upgraded to a newer release by using the ``--upgrade`` flag::

    > pip install --upgrade spydrnet
    
It can be installed from source archives or distributions available on `GitHub <https://github.com/byuccl/spydrnet/releases>`_ or
`PyPI <https://pypi.python.org/pypi/spydrnet>`_::

    > pip install spydrnet-<version>.tar.gz

or::

    > pip install spydrnet-<version>-py3-none-any.whl
    
It can also be installed from within the directory of its repository::

    > pip install .
    
or::

    > python setup.py install
    
Install in Developer Mode
-------------------------

If a development environment is desired, please make sure that any previous installations are uninstalled before proceeding::

    > pip uninstall spydrnet

SpyDrNet can be installed in editable mode from within the directory of its repository::

    > pip install -e .

Editable mode allows modification of the source to be reflected in the use of the module the next time that it is imported into Python. This functionality is convenient for development.
    
The project repository can be cloned using `Git <https://git-scm.com/>`_. The following commands clone the repository and enter its directory::

    > git clone https://github.com/byuccl/spydrnet.git
    > cd spydrnet


Optional Packages
-----------------

SpyDrNet depends on the following optional packages for additional functionality.

- `pytest <https://docs.pytest.org/>`_ provides automated test execution.
- `PLY <https://www.dabeaz.com/ply/>`_ provides a lexer and AST framework for parsing verilog (experimental).

To install SpyDrNet with all optional packages, execute the following command::

    $ pip install spydrnet[all]

Optional packages can also be installed separately.
