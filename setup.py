# Setup module for python DSA package.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_dsa",
    version="0.0.1",
    author="Chirag Chadha",
    author_email="chiragchadhairl@gmail.com",
    description="Common data structures and algorithms in Python",
    packages=setuptools.find_packages(),
)
