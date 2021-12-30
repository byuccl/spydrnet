import sys
import setuptools
import glob
import os

if sys.argv[-1] == "setup.py":
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (3, 6):
    python_version = "{}.{}".format(sys.version_info[0], sys.version_info[1])
    msg = (
        "SpyDrNet 1.0+ requires Python 3.6 or later ({} detected).\n\n".format(python_version)
    )
    sys.stderr.write(msg + "\n")
    sys.exit(1)

# Write the version information.
sys.path.insert(0, 'spydrnet')
import release
version = release.update_versionfile()
sys.path.pop(0)

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(':ref:','')

example_edif_files = list()
folder_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "spydrnet", "support_files"))
for filename in glob.glob(os.path.join(folder_path, "**", "*"), recursive=True):
    if os.path.isfile(filename) and os.path.getsize(filename) < 1024 * 10:
        example_edif_files.append("support_files/" + str(filename)[len(folder_path) + 1:].replace('\\', '/'))
        
extras_require = {
    "all": [
        "pytest",
        "ply",
    ],
    "pytest": ["pytest"],
    "ply": ["ply"],
}

if __name__ == "__main__":

    setuptools.setup(
        name=release.name.lower(),
        version=version,
        maintainer=release.maintainer,
        maintainer_email=release.maintainer_email,
        author=release.authors['Keller'][0],
        author_email=release.authors['Keller'][1],
        description=release.description,
        keywords=release.keywords,
        long_description=long_description,
        license=release.license,
        platforms=release.platforms,
        url=release.url,
        project_urls=release.project_urls,
        classifiers=release.classifiers,
        package_data={ 'spydrnet': ['VERSION'] + example_edif_files},
        packages=setuptools.find_packages(),
        extras_require=extras_require,
        python_requires='>=3.6',
        zip_safe=False
    )