.. _CONTRIBUTING.rst:

How to Contribute
=================

Thank you for your interest in contributing to SpyDrNet. We welcome your support
and hope that you have a great experience. Additionally we hope you feel as we
do that your work on SpyDrNet makes a positve impact on the greater community.

We ask all contributers to make respectful and constructive contributions in 
order to ensure a positive environment exists around SpyDrNet.

**some suggestions as you get started**

 * Make sure you have a recent version of python installed. We test against version 3.6 and up (as of SpyDrNet 1.10.0...before then we also supported Python 3.5).
 * Clone the repository and create a new branch on which to make changes.
 * Connect through Git Hub. The issues tab is the primary place for conversations and questions.
 * Make sure that there are tests for your code.
 * While we do not require 100% test coverage it is a good idea to strive to achive it.
 * Make sure that your code passes the Travis CI test before merging to master

**To start contributing please follow the following steps**

1. Create a github account
2. Clone the SpyDrNet repositoy
3. Otherwise fork the repository to make your changes.
4. Once you have made your changes make a pull request.
5. When the pull request has passed the tests it will be reviewed and merged. Note: we may have you request your code into a branch other than *master*


**Write (or other) privileges can be obtained**

*if*

you have made a few good contributions and plan to make more

*or*

you are a student working on the project in the BYU CCL

*and in either case*

upon request to the admins who can give write privlages.

If you don't know who the admins are and you feel that you qualify you can 
create an issue to request permissions.

Of course the admin's have the final say in granting permissions and reserve the
right to deny privileges for any reason or no reason at all even if the above 
criteria are met.

Testing
-------

We use pytest which can be installed through pip, to test the repository. Tests
are placed in the tests folders at an appropriate place in the repository. The
existing tests can be used as a template to create your own and the pytest
documentation can be referenced as well. Basically `import unittest` and then
declare your class and have it inherit from the `unittest.TestCase` like this
`class TestFeatureName(unittest.TestCase):` then make sure that your function
is called something that starts with `test_` like
`def test_some_functionality(self):`.

Exceptions and other features can be tested as well within the pytest framework.

