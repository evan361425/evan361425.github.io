# Custom MkDocs Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Some useful tools for my MkDocs.

## ImageUrlTemplate

Add domain on image's url, for example, in file `hello/my/essay.md`:

```md
![hello](my-file-name)
```

configuration:

```yaml
plugins:
- image_url_template:
    domain: https://imgs.blog.evan361425.com
```

will render to

```html
<img alt="hello" src="https://imgs.blog.evan361425.com/hello/my/essay/my-file-name.avif">
```

I use two scripts to convert image to `avif` format and upload to Cloudflare R2:

```sh
find imgs/src -name '*' -type f | xargs bash lib/scripts/image_processor.sh convert
node lib/scripts/upload_to_r2.js
```

## ClearNewline

Remove newline after full-width punctuation.

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

> The caption text, it will ignore any html effect include [links](this will be ignored)
```

Using `/` as prefix will ignore using caption, for example:

```md
| header 1 | header 2 |
| -------- | -------- |
| a        | b        |

> /This is a real blockquote
```

## SimpleServe

Help serving the specific source only.

search `serve_simple` to see example in [mkdocs.yaml](../mkdocs.yaml).

## Install

```shell
pip install -e lib
```
