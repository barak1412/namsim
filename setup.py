from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def post_install_decorator(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.
    It modifies the run() method so that it will change the configuration paths.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        print("Hello, developer, how are you? :)")
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


setup(
    # Information
    name="namsim",
    version="1.0.0",
    author="Barak David",
    license="MIT",
    keywords="Name similarity mock-up library.",
    packages=['namsim', 'namsim.wrapper']
)
