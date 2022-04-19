from setuptools import setup

setup(
    name=               "libdogecoin",
    version=            "0.3",
    description=        "Python interface for the libdogecoin C library",
    author=             "Jackie McAninch",
    author_email=       "jackie.mcaninch.2019@gmail.com",
    license=            "MIT",
    python_requires=    ">=3.8.10",
    packages=           ["libdogecoin"],
    package_dir=        {"":"bindings/py_wrappers"},
    package_data=       {"": ["libdogecoin.so"]}
)