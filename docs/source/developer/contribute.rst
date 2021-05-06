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
5. Commit those changes to the pull request
6. Update the tag
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

`make html`

and

`make latexpdf`

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

`git describe`

**Creation**

>>> git tag -a v1.5.0 -m "SpyDrNet 1.5.0"

**Push your changes to the tags**

>>> git push --tags

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

Publishing the packages to Pypi
-------------------------------

The packages need to be published to Pypi to be installable via pip. On pypi.org
there is a guide on uploading packages. Follow the instructions there to upload
to the test pip server then the production server.

Publishing the documentation
----------------------------

This is easiest on Linux (or at least not Windows, MacOS works fine as well)

Checkout the gh-pages branch create a new folder with the release number as the
name. Copy the `docs/build/html` folder into the newly created folder.

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
