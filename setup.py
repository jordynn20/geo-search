from setuptools import setup, find_packages

setup(
    name="geo-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.30.0,<3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "geo-search=geo_search.search_geo:main",
        ],
    },
    author="Jordyn Niemiec",
    description="A command-line tool for searching NCBI GEO datasets.",
)
