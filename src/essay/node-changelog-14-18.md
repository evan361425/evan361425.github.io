---
tags: Changelog
description: Node.js 從 14 版升到 18 版的注意事項。
image: https://i.imgur.com/lNoXVcw.png
---

# Node.js 從 14 升 18 的注意事項

Node.js 14 版將於 [2023-04-30](https://endoflife.date/nodejs) 不再支援，
同時 16 版本將於 2023-09-11 過期，
勢必會有許多人從 Node.js 14 版本直接升到 18。

這裡會列出一些需要注意的點。

??? question "還有其他地方也有摘要整理嗎"

    當然有，你除了直接吃生魚片：

    - Node.js 16
        - [Changelog](https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V16.md#16.0.0)
    - Node.js 18
        - [Changelog](https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V18.md#18.0.0)

    也可以吃其他人煮過的：
    
    - Node.js 16
        - 官方在 2021 發表了一篇文章摘要的[注意事項](https://medium.com/the-node-js-collection/node-js-16-available-now-7f5099a97e70)。
        寫得很好，可惜沒有 Node.js 18，
        而且也在 2022 表達[不會再發表新文章](https://medium.com/the-node-js-collection/archived-node-js-medium-collection-6f8ddd6723a7)。
        - [RedHat 官方文件](https://access.redhat.com/documentation/zh-tw/red_hat_build_of_node.js/18/html-single/release_notes_for_node.js_18/index#runtime_deprecation_of_string_coercion_in_literal_fs_literal_methods_for_writing_or_appending_files)
    - Node.js 18
        - 五大新功能的[部落格文章](https://betterprogramming.pub/5-major-features-of-node-js-18-5f4a164cc9fc)
        - [官方文件](https://nodejs.org/en/blog/announcements/v18-release-announce)
        - [RedHat 官方文件](https://access.redhat.com/documentation/zh-tw/red_hat_build_of_node.js/18/html-single/release_notes_for_node.js_18/index#runtime_deprecation_of_string_coercion_in_literal_fs_literal_methods_for_writing_or_appending_files)

## ECMA Script

Node.js 14 到 18 支援的協定**從 ES2019 升到 ES2023**，
但要注意 14 並不是每個功能都不支援，例如 14 支援 private class method，
但這卻是 ES2022 才開始支援的 API：

```js
class MyClass {
    #myPrivateField = 'this is private';
}
```

詳細的對照，你可以到 [node.green](https://node.green/#ES2019) 查看。

## V8

Node.js 每次升版都會更新 [V8](https://v8.dev/) 的版本，
所有版本的更新都可以到 [Chrome road-map](https://chromestatus.com/roadmap) 查看。
Node.js 14 使用的版本是 8.6 將會升到 Node.js 18 的 10.1。

> 所謂 V8 10.1 版本，
> 就是對應 Chrome 101 版，詳見 [V8 的 blog](https://v8.dev/blog/discontinuing-release-posts)。

大致差異在於對於 ES 的適應和效能調校。

## TypeScript

TypeScript 的設定也會因為 Node.js 升版而有改變，建議可以參考官方推薦的設定檔：

-   [Node.js 18](https://github.com/tsconfig/bases/blob/main/bases/node18.json)；
-   [ESM](https://github.com/tsconfig/bases/blob/main/bases/esm.json)，實際上 ESM 的設定很複雜，
    可以參考有在維護的 [template-node-ts](https://github.com/tsconfig/bases/blob/main/bases/strictest.json)
    和網路上的一些整理文章，例如這篇 [Gist](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c)；
-   對程式碼有潔癖的[設定](https://github.com/tsconfig/bases/blob/main/bases/strictest.json)。ㄋ

## 一些功能

這裡整理一些有趣的新功能：

-   異步的 setTimeout

    ```js
    import { setTimeout } from 'timers/promises';
    async function run() {
        await setTimeout(5000);
    }
    ```

-   [Event 和 EventTarget](https://nodejs.org/dist/latest-v18.x/docs/api/events.html#eventtarget-and-event-api) 的實作
-   預設會設定服務的 Timeout：
    -   `headersTimeout`：讀取 HTTP Header 超過 60 秒後會中斷連線
    -   `requestTimeout`：處理 HTTP 請求超過 5 分鐘後會中斷連線
-   [Blob](https://nodejs.org/dist/latest-v18.x/docs/api/buffer.html#class-blob)，類似 Buffer，
    但是允許多個線程對他進行讀取和修改。
-   [BroadcastChannel](https://nodejs.org/dist/latest-v18.x/docs/api/worker_threads.html#class-broadcastchannel-extends-eventtarget)，類似 EventTarget，
    但是適合多線程的傳遞資訊。

下面這裡有趣但還在[開發階段](https://nodejs.org/dist/latest-v18.x/docs/api/documentation.html#stability-overview)的功能：

-   透過 [Web Crypto API](https://www.w3.org/TR/WebCryptoAPI/) 來進行密碼學的應用，
    Node.js 一直都希望弭平瀏覽器和後端的差異。
-   [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch)，
    也是為了弭平和瀏覽器的差異，允許快速而簡單

    ```js
    const myInit = {
        method: "GET",
        headers: {
            Accept: "image/jpeg",
        },
        mode: "cors",
        cache: "default",
    };

    fetch(new Request("flowers.jpg"), myInit)
    ```

-   原生單元測試框架：[Test Runner](https://nodejs.org/dist/latest-v18.x/docs/api/test.html)

    ```js
    import test from 'node:test';
    import assert from 'assert';

    test('synchronous passing test', (t) => {
        // This test passes because it does not throw an exception.
        assert.strictEqual(1, 1);
    });
    ```