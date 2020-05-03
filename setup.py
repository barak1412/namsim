import atexit
import os
import sys
import fileinput
import fnmatch
import glob
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info


LIB_NAME = "namsim"
NAMSIM_DATA_DIRECTORY = "data"
NAMSIM_CONF_DIRECTORY = "default_namsim_conf"


def post_install_operations(lib_path):
    # TODO: workaround to exit in library creation process
    if 'site-packages' not in lib_path:
        return

    # set conf path and replace slash to backslash to support UNIX systems
    conf_dir_path = os.path.join(lib_path, NAMSIM_DATA_DIRECTORY, NAMSIM_CONF_DIRECTORY)
    conf_dir_path = conf_dir_path.replace(os.sep, '/')

    # change paths in all conf .xml files
    file_pattern = "*.xml"
    for path, dirs, files in os.walk(conf_dir_path):
        for filename in fnmatch.filter(files, file_pattern):
            full_file_path = os.path.join(path, filename)
            print(full_file_path)
            # replace stub with the actual path
            stub_name = 'STUB_PATH'

            # Read in the file
            with open(full_file_path, 'r') as file:
                file_data = file.read()

            # Replace the target string and fix slash direction based
            file_data = file_data.replace(stub_name, conf_dir_path)

            # Write the file out again
            with open(full_file_path, 'w') as file:
                file.write(file_data)


def post_install_decorator(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.
    It modifies the run() method so that it will change the configuration paths.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        def find_module_path():
            for p in sys.path:
                if os.path.isdir(p) and LIB_NAME in os.listdir(p):
                    return os.path.join(p, LIB_NAME)
        orig_run(self)
        lib_path = find_module_path()
        post_install_operations(lib_path)

    command_subclass.run = modified_run
    return command_subclass


@post_install_decorator
class CustomDevelopCommand(develop):
    pass


@post_install_decorator
class CustomInstallCommand(install):
    pass


@post_install_decorator
class CustomEggInfoCommand(egg_info):
    pass


setup(
    name="namsim",
    version="1.0.0",
    author="Barak David",
    license="MIT",
    keywords="Name similarity mock-up library.",
    packages=['namsim', 'namsim.wrapper', 'namsim.data'],
    package_date={'data': ['default_namsim_conf/*']},
    include_package_data=True,
    cmdclass={
        'develop': CustomDevelopCommand,
        'install': CustomInstallCommand,
        'egg_info': CustomEggInfoCommand
    }
)
