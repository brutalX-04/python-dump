from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

VERSION = "0.0.1"
DESCRIPTION = "This library was created to shorten the process of creating Python scripts."

setup(
    name="XModLb",
    version=VERSION,
    description=DESCRIPTION,
    author="Rizky Nurahman",
    author_email="rizky110704@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/XMod-04/XModLb",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "short"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)