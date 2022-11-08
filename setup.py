import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kenpompy",
    version="0.3.2",
    author="Jared Andrews",
    author_email="jared.andrews07@gmail.com",
    description="A python package for scraping kenpom.com NCAA basketball data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j-andrews7/kenpompy",
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers"
    ],
    install_requires = ["mechanicalsoup", "pandas", "bs4"],
    python_requires='>=3.8',
)