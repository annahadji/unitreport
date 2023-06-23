"""Distribution script for unitreport."""
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="unitreport",
    version="0.1.1",
    author="annahadji",
    author_email="annahadji@users.noreply.github.com",
    description="A small unittest-based tool for generating single page html reports in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="static unittest report generator Markdown plots tables",
    url="https://github.com/annahadji/unitreport",
    packages=["unitreport"],
    package_data={"unitreport": ["templates/**"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
    install_requires=["jinja2", "markdown", "matplotlib"],
)
