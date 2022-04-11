.. include:: ../../../CONTRIBUTING.rst


Creating a Release
==================

This section aims to help you do a spydrnet release, meaning you make the latest code and documentation available. The steps are listed in what seems to be the best order of operation. Steps which need more explanation are highlighted below.

1. Merge each contributors' branches into one branch (the 'next_release' branch)
2. run `git merge master` while the next-release branch is checked out.
3. :ref:`update_release_notes`
4. :ref:`update_documentation` and ensure it can build properly
5. On Github, create a pull request with the updated code in the next_release branch.
6. Accept and merge the pull request when the checks have finished.
7. Move to the master branch using `git checkout master`
8. :ref:`create_and_update_tag`
9. :ref:`build_documentation`
10. :ref:`build_package` (this will update the documentation’s version number)
11. :ref:`publish_packages`
12. :ref:`github_release`
13. :ref:`publish_documentation`

.. _update_release_notes:

Update the Release Notes
-------------------------

The release notes file called RELEASE.rst should be updated to outline what has
been acomplished. The date and version number should be included and other 
information as needed can be entered as well.

SpyDrNet uses a Major.Minor.Bug versioning scheme where minor 
version updates do not break the existing API and major version updates may
break it. Bug fixes do not add substantial new functionality, but rather fix 
broken functionality.

.. _update_documentation:

Update the Documentation
--------------------------

The documentation pulls from doc strings as well as .rst files in the build so
this step is important. The documentation is built using a makefile in the docs
folder.

Before building the documentation run `make clean` to clear away the old files.

Before proceeding, ensure that both of the following are successful (make they execute without errors. Try to minimize the warnings as well):

>>> make html

and

>>> make latexpdf

if you are missing packages run:

>>> make install

You may also need to run 'sudo apt install latexmk' and 'apt install texlive-latex-extra' to be able to create the pdf file.

The generated files can be found in the build folder. Take a look at them and make sure everything looks good. Later, these commands will be run again, and the html files put online and pdf files added to the Github release files.

.. _create_and_update_tag:

Create and Update the Tag
--------------------------

Be sure you are on the master branch.

Tags are used to label the release. When all changes are merged into the main branch, create a new tag. In the examples below, replace 1.5.0 with the version number you are releasing.

**To see the current version number**

>>> git describe

**Create the tag**

>>> git tag -a v1.5.0 -m "SpyDrNet 1.5.0"

**Push your changes to the tags**

>>> git push --tags

If you mess up, you can use the following instructions to force update your tag

**Updating**

>>> git tag -a v1.5.0 -m "SpyDrNet 1.5.0" -f

>>> git push --tags -f

.. _build_documentation:

Build the Documentation
------------------------

Make sure you are in the docs directory

>>> cd docs

then run the following:

>>> make clean
>>> make latexpdf
>>> make html

Make sure that each one executes without errors. Try to minimize warnings as well, although the most important thing is that the documentation looks the way you want it to.

.. _build_package:

Build the Python Package
-------------------------

Refer to pypi.org if necessary. They have a tutorial called “uploading packages”

Upgrade pip if needed.

>>> python3 -m pip install --upgrade pip

Make sure everything is up to date

>>> python3 -m pip install --user --upgrade setuptools wheel

Make the python archive package:

>>> python3 setup.py sdist bdist_wheel

The build files will be stored in the following directories 

spydrnet/build and spydrnet/dist

.. _publish_packages:

Publish the Packages to Pypi
-----------------------------

The packages need to be published to Pypi in order to be installable via pip. On the `Pypi website <https://packaging.python.org/tutorials/packaging-projects/>`_ there is a guide on uploading packages. You will need an account for this. Follow the instructions there to upload to the test pip server and then the production server.

If you have an account and know what you are doing, use the command below :

>>> python3 -m twine upload dist/*

And then input your username and password for Pypi.

To install the python package to check for success, use:

>>> python3 -m pip install spydrnet

Then go to the release on the Pypi website through your account. Download the .whl file and the .tar.gz file. These will be used in the next step.

.. _github_release:

Create a Github Release
------------------------

Releases can be created on Github. On the releases tab you can draft a new
release. You can then select the existing tag with the release number you want
to release.

The release should be named `SpyDrNet 1.5.0` where 1.5.0 is replaced with the
proper release number.

Enter a description–it could just be a reiteration of the release notes or other relevant information.

Three files should be added as assets to the new release:
    1. The .tar.gz file from the previous step
    2. The .whl file from the previous step
    3. The spydrnet_reference pdf document created in the :ref:`build_documentation` step. Go to docs/latex folder, change the `spydrnet_reference.pdf` name to `spydrnet_reference-new_release_number.pdf`, and then copy it to the assets under the new release.

.. _publish_documentation:

Publish the Documentation
--------------------------

This is easiest on Linux (or at least not Windows, MacOS works fine as well)

Make sure you are still on the Master branch and that everything in the html folder is up-to-date.
If not, re-run the instructions in :ref:`build_documentation`.

Move to the gh-pages branch using

>>> git checkout gh-pages

Create a new folder with the release number as the name. Move the contents of the `docs/build/html` folder into the newly created folder. Then delete the html folder (which should be empty).

(If html folder doesn't contain the latest pages, it could be that the html folder wasn't deleted from the previous release, delete the folder, commit the changes and repeat the steps above)

The documentation is built from a stable link which will need to be updated to point to the new documentation.

Check which version of the documentation the stable link points to

>>> ls -lha

To update the stable link, remove it first (watch syntax here very carefully, a
terminating \ could make the command delete the folder's contents instead of the
link)

>>> rm stable

Then create a link to the new folder

>>> ln -s version.number stable

Then add, commit, and push the newly created folder and the updated stable link to the git repository, just to the gh-pages branch.
