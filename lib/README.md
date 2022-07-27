# Custom Setting

## Mermaid

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An [MkDocs](https://www.mkdocs.org/) plugin that renders textual graph
descriptions into [Mermaid](https://mermaid-js.github.io/mermaid) graphs
(flow charts, sequence diagrams, pie charts, etc.).

> This is a fork from
> [fralau's excellent project](https://github.com/fralau/mkdocs-mermaid2-plugin).

## Figcaption

Add figure's caption by `alt`, for example:

```md
![My Caption](url)
```

Ignore caption by leading `!`, for example:

```md
![!Alt only](url)
```

## TableCaption

Add caption in table by next blockquote, for example:

```md
| header 1 | header 2 |
| -------- | -------- |
| a        | b        |

> The caption text, it will ignore any html effect include [links](this will ignored)
```

Using `/` as prefix will ignore using caption, for example:

```md
| header 1 | header 2 |
| -------- | -------- |
| a        | b        |

> /This is a real blockquote
```

## SimpleServe

Help serving the specific source only

see [serve.json](../serve.json) as example.

## Install

```shell
pip install -e lib
```
