"""
Setup file

The code is licensed under the MIT license.
"""

from os import path
from setuptools import setup

# Content of the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

# Setup
setup(
    name="meteostat-stations",
    version="0.0.2",
    author="Meteostat",
    author_email="info@meteostat.net",
    description="A list of public weather stations everyone can edit and share.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meteostat/weather-stations",
    keywords=["weather", "climate", "data", "timeseries", "meteorology"],
    python_requires=">=3.5.0",
    package_dir={"stations": "lib"},
    packages=["stations"],
    include_package_data=True,
    install_requires=["meteostat==1.5.7"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
