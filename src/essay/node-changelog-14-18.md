---
tags: Changelog
---

# Node.js 從 14 升 18 的注意事項

Node.js 14 版將於 [2023-04-30](https://endoflife.date/nodejs) 不再支援，
同時 16 版本將於 2023-09-11 過期，
勢必會有許多人從 Node.js 14 版本直接升到 18。

這裡會列出一些需要注意的點。

!!! info "還有其他地方也有摘要整理嗎"

    當然有，你除了直接吃生魚片，也可以吃其他人煮過的：

    - Node.js v18 [Changelog](https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V18.md#18.0.0)
    - Node.js v16 [Changelog](https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V16.md#16.0.0)

    官方在 2021 發表了一篇文章摘要 [Node.js 16 的注意事項](https://medium.com/the-node-js-collection/node-js-16-available-now-7f5099a97e70)。

    寫得很好，可惜沒有 Node.js 18，
    而且也在 2022 表達[不會再發表新文章](https://medium.com/the-node-js-collection/archived-node-js-medium-collection-6f8ddd6723a7)。

## ECMA Script

Node.js 14 到 18 支援的協定**從 ES2019 升到 ES2023**，
但要注意 14 並不是每個功能都不支援，例如 14 支援 private class method：

```js
class MyClass {
    #myPrivateField = 'this is private';
}
```

詳細的對照，你可以到 [node.green](https://node.green/#ES2019) 查看。

## V8

Node.js 每次升版都會更新 [V8](https://v8.dev/) 的版本，
Node.js 14 使用的版本是 8.6 將會升到 10.1。

[tsconfig 設定推薦](https://www.npmjs.com/package/@tsconfig/node18)，
需要注意 CommonJS 和 ESModule 的差異
