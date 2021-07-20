.. include:: ../../../CONTRIBUTING.rst


Creating a Release
==================

So you have code that works and improves SpyDrNet. Now you want to make it 
publically available. This section aims to help you do just that. The steps
are listed in what appears to us at this time to be the best order of
operations. Steps which need more explanation are highlighted below.

1. run `git merge master` while the pre-release branch is checked out.
2. Create a pull request with the updated code in the pre-release branch.
3. Update the release notes
4. Update the documentation and ensure it can build properly
5. Commit and push those changes to the pull request. Accept the pull request when the checks have finished.
6. Checkout to master branch and update the tag
7. Build the python package (this will update the documentation’s version number)
8. Build the documentation
9. Create the release on Github
10. Publish the packages
11. Publish the documentation

Updating the documentation
--------------------------

The documentation pulls from doc strings as well as .rst files in the build so
this step is important. The documentation is built using a makefile in the docs
folder.

Before building the documentation run a `make clean` to clear away files that 
may mask warnings and errors and ensure the process is smooth.

For the release ensure that both:

>>> make html

and

>>> make latexpdf

if you are missing packages run:

>>> make install

You may also need to run 'sudo apt install latexmk' and 'apt install texlive-latex-extra' to be able to create the pdf file.

build the documentation without error as the html version will be put online at 
the time of release and the pdf should be included in the releases files on
Github

The output in the build folder can be examined to ensure that everything looks
good.

Updating the Release Notes
--------------------------

The release notes file called RELEASE.rst should be updated to outline what has
been acomplished. The date and version number should be included and other 
information as needed can be entered as well.

SpyDrNet uses a Major.Minor.Bug versioning scheme where minor 
version updates do not break the existing API and major version updates may
break it. Bug fixes do not add substantial new functionality, but rather fix 
broken functionality.

Creating and updating the tag
-----------------------------

Tags are used to put a label on the release, the tag is used when building the
documentation. If a new commit is pushed to the branch the tag will be left
on the previous commit. In these cases the tag can be updated.

In the examples below, replace 1.5.0 with the version number you want to release

**To see the current version number**

>>> git describe

**Creation**

>>> git tag -a v1.5.0 -m "SpyDrNet 1.5.0"

**Push your changes to the tags**

>>> git push --tags

If you mess up, you can use the following instructions to force update your tag

**Updating**

>>> git tag -a v1.5.0 -m "SpyDrNet 1.5.0" -f

>>> git push --tags -f

Building the python package
---------------------------

Refer to pypi.org They have a tutorial called “uploading packages”

Upgrade pip if needed.

>>> python3 -m pip install --upgrade pip

Make sure everything is up to date

>>> python3 -m pip install --user --upgrade setuptools wheel

Make the python archive package:

>>> python3 setup.py sdist bdist_wheel

The build files will be stored in the following directories 

spydrnet/build and spydrnet/dist

.. _Build:

Building the documentation
--------------------------

Make sure you are in the docs directory

>>> cd docs

then run the followings:

>>> make clean
>>> make latexpdf
>>> make html

Make sure that each one executes and doesn't have errors. It's also nice if 
the warnings are minimized as well, of course the most important thing is that the
documentation looks the way you want.

Creating a Github Release
-------------------------

Releases can be created on github. On the releases tab you can draft a new
release. You can then select the existing tag with the release number you want
to release.

The release should be named `SpyDrNet 1.5.0` where 1.5.0 is replaced with the
proper release number.

A description should be entered as well. It could just be a reiteration of the
release notes or other relevant information.

Three files should be added as assets to the new release:

Two files will be generated when the repository is pushed to Pypi. A tar.gz file and a .whl file. 
Uploead these two files after performing the next step of `Publising the packages to Pypi`

Go to docs/latex folder, copy the `spydrnet_reference.pdf` to the assets under the new release,
and changes its name to `spydrnet_reference-new_release_number.pdf`. If the pdf file doesn't exist, run:

>>> make latexpdf

in the /docs folder

Publishing the packages to Pypi
-------------------------------

The packages need to be published to Pypi to be installable via pip. On the `Pypi website <https://packaging.python.org/tutorials/packaging-projects/>`_
there is a guide on uploading packages. You will need an account for this. Follow the instructions there to upload
to the test pip server then the production server.

If you have an account and know what you are doing, use the command below :

>>> python3 -m twine upload dist/*

And then input your username and password for Pypi.

To install the python package to check for success, use:

>>> python3 -m pip install spydrnet

Go to the release on the Pypi website through your account. Download the .whl file and the .tar.gz file.
Add them as assets to the new release at GitHub.com

Publishing the documentation
----------------------------

This is easiest on Linux (or at least not Windows, MacOS works fine as well)

Make sure you are still in the Master branch and that everything in the html folder is up-to-date.
If not, re-run the instructions in :ref:`Build`.

Checkout the gh-pages branch create a new folder with the release number as the
name. Move the `docs/build/html` folder into the newly created folder. 
Make sure to delete the html folder after you are finished.

(If html folder doesn't contain the latest pages, it could be that the html folder wasn't deleted from the previous release,
delete the folder, commit the changes and repeat the steps above)

The documentation is built from the stable link so the stable link will need to
be updated to point to the newly updated documentation.

Check which version of the documentation the stable link points to

>>> ls -lha

to update the stable link remove it first (watch syntax here very carefully, a
terminating \ could make the command delete the folder's contents instead of the
link)

>>> rm stable

then create a link to the new folder

>>> ln -s version.number stable

run git add to add the newly created folder and the stable link

push your changes to the git repository, just to the ghpages branch.
