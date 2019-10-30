import os
import sys


from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.rst")) as f:
        README = f.read()
    with open(os.path.join(here, "CHANGES.txt")) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ""


install_requires = []
docs_extras = []
tests_require = ["pytest"]
testing_extras = tests_require + ["flake8", "black"]

setup(
    name="evilunit",
    version="0.1.4",
    description="evil parts of unittest",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="unittest, test",
    author="podhmo",
    author_email="",
    url="https://github.com/podhmo/evilunit",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"testing": testing_extras, "docs": docs_extras},
    tests_require=tests_require,
    test_suite="evilunit.tests",
    entry_points="""
""",
)
