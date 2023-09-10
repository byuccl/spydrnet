import sys
import setuptools
from pathlib import Path

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

support_files = []
folder_path = Path(Path(__file__).parent).joinpath("spydrnet", "support_files")
for filename in Path.glob(folder_path, "**/*"):
    if filename.is_file() and \
        (filename.stat().st_size < 1024 * 10 or "architecture_libraries" in str(filename)):
        support_files.append("support_files/" + str(filename)[len(str(folder_path)) + 1:].replace('\\', '/'))

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
        package_data={ 'spydrnet': ['VERSION'] + support_files},
        packages=setuptools.find_packages(),
        extras_require=extras_require,
        python_requires='>=3.6',
        zip_safe=False
    )