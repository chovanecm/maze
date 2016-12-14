from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    author="Martin Chovanec",
    author_email="chovamar@fit.cvut.cz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
    description="Maze",
    long_description=long_description,
    license="LGPL",
    url="https://github.com/chovanecm/maze",
    name="maze",
    keywords="maze",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "maze = gui:main"
        ]
    },
    install_requires=["numpty", "pytest", "matplotlib", "PyQt5"],
    version="0.3"
)
