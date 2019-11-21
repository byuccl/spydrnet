import sys
import setuptools

if sys.argv[-1] == "setup.py":
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (3, 6):
    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    msg = (
        f"SpyDrNet 1.0+ requires Python 3.6 or later ({python_version} detected).\n\n"
    )
    sys.stderr.write(msg + "\n")
    sys.exit(1)

# Write the version information.
sys.path.insert(0, 'spydrnet')
import release
version = release.update_versionfile()
sys.path.pop(0)

with open("README.md", "r") as fh:
    long_description = fh.read()

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
        long_description_content_type="text/markdown",
        license=release.license,
        platforms=release.platforms,
        url=release.url,
        project_urls=release.project_urls,
        classifiers=release.classifiers,
        package_data={ 'spydrnet': ['VERSION']},
        packages=setuptools.find_packages(),
        python_requires='>=3.6',
        zip_safe=False
    )