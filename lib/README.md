# Custom Setting

## Mermaid

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An [MkDocs](https://www.mkdocs.org/) plugin that renders textual graph
descriptions into [Mermaid](https://mermaid-js.github.io/mermaid) graphs
(flow charts, sequence diagrams, pie charts, etc.).

> This is a fork from
> [fralau's excellent project](https://github.com/fralau/mkdocs-mermaid2-plugin).

## Figcaption

Add caption in figure by `alt`, example:

```md
![My Caption](url)
```

Ignore caption by leading `!`, example:

```md
![!Alt only](url)
```

## Tablecaption

Add caption in table by first header, example:

```md
| My Caption~header 1 | header 2 |
| ------------------- | -------- |
| a                   | b        |
```

> Using `~` as delimiter.

## Install

```shell
pip install -e lib
```
