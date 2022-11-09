Linting
=======

SpyDrNet developers strive to provide high quality code that follows a general coding standard and does not contain errors. To help accomplish this goal, the `Pylint <https://pylint.org/>`__ python package is used.

Running Pylint
--------------

There are many ways to execute pylint to lint code. SpyDrNet source code can be linted by executing the following command from within the directory of the repository::

    pylint spydrnet/
    
This will run pylint in its most basic form, without any specified options. A number of options are preffered that are specific to SpyDrNet's needs. These options are found in the `.pylintrc` file, and can be used with the following command::

   pylint --rcfile=.pylintrc spydrnet/

Pylint will then provide a score from 0.0 to 10.0 for your code. The best way to understand how this score is produced is to run pylint on SpyDrNet, or on any Python script. Pylint can also be run on individual files or directories with the following commands::

   pylint <directory_name>/
   pylint <file_name>.py

It is strongly encouraged to run pylint on any code that you change or create that will be added into the SpyDrNet repository, and ensure that the code scores well (getting 10.0 is not terribly difficult). This not only improves the SpyDrNet codebase, but will improve your own skills as a competant programmer.

Pylint, along with pytest, will be run every time code is pushed to the GitHub repository with GitHub actions (as specificed in the `.github/workflows/pylint.yml` file in the root SpyDrNet directory).

Viewing Pylint score for each release
-------------------------------------
On the `byuccl/spydrnet <https://github.com/byuccl/spydrnet/actions>`__ page, navigate to the "Actions" tab. From there, you should be able to select the "Pylint" workflow and view all jobs within that workflow. Open up a job, and then find the "Analysing the code with pylint" tab. Here, all pylint output can be found for each push done for the repository. 