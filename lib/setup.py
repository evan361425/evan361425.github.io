from setuptools import setup, find_packages


VERSION = "0.1.0"


def readme():
    """print long description"""
    with open("README.md") as f:
        return f.read()


LONG_DESCRIPTION = (
    "A mkdocs plugin that do things in the markdown file."
    "Interprets mermaid graphs and add figcaption."
    "This is a fork of the fralau's excellent project."
)

setup(
    name="mkdocs-evan361425-plugin",
    version=VERSION,
    description="A MkDocs plugin for interprets mermaid graphs and add figcaption",
    long_description=LONG_DESCRIPTION,
    keywords="mkdocs python markdown mermaid",
    url="https://github.com/evan361425/evan361425.github.io",
    author="pugong, Fralau, evan361425",
    author_email="pugong.liu@gmail.com, fralau2035@yahoo.com, sevan361425@gmail.com",
    license="MIT",
    python_requires=">=3.5",
    install_requires=[
        "setuptools>=18.5",
        "beautifulsoup4>=4.6.3",
        "mkdocs>=1.0.4",
        "jsbeautifier",
        "pyyaml",  # for testing
        "mkdocs-material",  # for testing
        "requests",
        "pymdown-extensions >= 8.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["*.tests"]),
    entry_points={
        "mkdocs.plugins": [
            "mermaid = evan361425.mermaid:MarkdownMermaidPlugin",
            "figcaption = evan361425.figcaption:MarkdownFigcaptionPlugin",
            "tablecaption = evan361425.tablecaption:MarkdownTablecaptionPlugin",
            "serve_simple = evan361425.serve_simple:MarkdownServeSimplePlugin",
        ]
    },
)
