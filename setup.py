from setuptools import setup


setup(
    name="namsim",
    version="1.0.0",
    author="Barak David",
    license="MIT",
    keywords="Name similarity mock-up library.",
    packages=['namsim', 'namsim.wrapper', 'namsim.data', 'namsim.constants'],
    include_package_data=True,
    python_requires='>=3'
)
