import os

# Version information
name = 'spydrnet'
version = "UNSPECIFIED"
date = "UNSPECIFIED"

# Declare current release as a development release.
# Change to False before tagging a release; then change back.
dev = False

description = "Python package for analyzing and transforming netlists"
license = 'BSD'
authors = {'Keller': ('Andrew Keller', 'andrewmkeller@byu.edu'),
           'Skouson': ('Dallin Skouson', 'skousond@gmail.com'),
           'Wirthlin': ('Michael Wirthlin', 'wirthlin@byu.edu')}
maintainer = "SpyDrNet Developers"
maintainer_email = "spydrnet-discuss@googlegroups.com"
url = 'https://byuccl.github.io/SpyDrNet'
project_urls = {
    "Bug Tracker": "https://github.com/byuccl/SpyDrNet/issues",
    "Documentation": "https://byuccl.github.io/SpyDrNet",
    "Source Code": "https://github.com/byuccl/SpyDrNet",
}
platforms = ['Linux', 'Mac OSX', 'Windows', 'Unix']
keywords = ['Netlist', 'Analysis', 'Transformation',
            'netlist', 'fpga', 'primitives', 'module', 'port',]
classifiers = [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Education",
            "Topic :: Scientific/Engineering",
            'Topic :: Scientific/Engineering :: Information Analysis',
            "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ]


directory = os.path.dirname(os.path.abspath(__file__))
version_filename = os.path.join(directory, "VERSION")

def load_versionfile():
    global version
    global date
    if os.path.isfile(version_filename):
        with open(version_filename) as fi:
            version = fi.readline().strip()[1:]
            date = fi.readline().strip()
            
load_versionfile()

def update_versionfile():
    import datetime
    import time
    import subprocess
    
    global version
    global date
    
    date_info = datetime.datetime.utcfromtimestamp(int(os.environ.get('SOURCE_DATE_EPOCH', time.time())))
    date = time.asctime(date_info.timetuple())

    #check for git on path
    git_exists = False
    for path in os.environ['PATH'].split(os.pathsep):
        exe_file = os.path.join(path, 'git')
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            git_exists = True
        else:
            exe_file = os.path.join(path, 'git.exe')
            if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
                git_exists = True
            
    if git_exists:
        git_subprocess = subprocess.Popen(["git", "describe"], shell=True, cwd=directory, text=True, stdout=subprocess.PIPE)
        git_describe_output = git_subprocess.stdout.read()

        git_version = git_describe_output.strip()
        if git_version.startswith('v'):
            version_file = os.path.join(directory, "VERSION")
            with open(version_file, 'w') as fh:
                fh.write(git_version + '\n')
                fh.write(date + '\n')
            version = git_version[1:]
            
    return version
    
if __name__ == '__main__':
    update_versionfile()