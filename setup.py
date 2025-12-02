from setuptools import setup, find_packages

setup(
    name="geo-search-tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "geo-search=geo_search.cli:main"
        ]
    },
    author="Jordyn Niemiec",
    description="A command-line tool for searching NCBI GEO datasets.",
)
