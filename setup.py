from setuptools import setup


setup(
    name="namsim",
    version="1.0.0",
    author="Barak David",
    license="MIT",
    keywords="Name similarity mock-up library.",
    packages=['namsim', 'namsim.wrapper', 'namsim.data', 'namsim.namsim'],
    package_data={'data': ['default_namsim_conf/*', 'bin/*']},
    include_package_data=True
)
