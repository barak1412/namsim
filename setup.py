from setuptools import setup


setup(
    name="namsim",
    version="1.0.0",
    author="Barak David",
    license="MIT",
    keywords="Name similarity mock-up library.",
    packages=['namsim', 'namsim.wrapper', 'namsim.data'],
    package_date={'data': ['default_namsim_conf/*']},
    include_package_data=True
)
