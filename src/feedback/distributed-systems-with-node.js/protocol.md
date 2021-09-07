# Protocol

> 分散式系統中，很重要的一塊是「不同的服務間，彼此的溝通方式是什麼？」
> 比起撰寫完整又清楚的 API 文件，有沒有什麼好方法可以讓服務和服務之間同步 API？

以下討論皆假設：溝通是透過網路，且以 HTTP 協定為基礎。

## OSI (Open Systems Interconnection)

- 應用層（Application Layer）
- 表達層（Presentation Layer）
- 會議層（Session Layer）
- 傳輸層（Transport Layer）
- 網路層（Network Layer）
- 資料連結層（Data Link Layer）
- 實體層（Physical Layer）

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                             Data Frame                                                │
├─────────────────┬─────────┬───────────┬───────────┬───────────────────────────────────────┬───────────┤
│        DLH      │    H3   │     H4    │     H5    │      H6      │ H7 │       DATA        │    DLT    │
│                 │         │           │           │         ┌────┐         ┌────┐         │           │
│                 │         │           │           │ chunk 1 │Sync│ chunk 2 │Sync│ chunk N │           │
│                 │         │           │           └─────────┘    └─────────┘    └─────────┤           │
│                 │         │           │                                                   │           │
├─────────────────┼─────────┼───────────┼───────────┬──────────────┬────────────────────────┼───────────┤
│    Data Link    │ Network │ Transport │  Session  │ Presentation │       Application      │ Data Link │
├─────────────────┼─────────┼───────────┼───────────┼──────────────┼────────────────────────┼───────────┤
│                 │         │           │ Uncurrent │  Uncurrent   │                        │           │
├─────────────────┼─────────┼───────────┼───────────┴──────────────┴────────────────────────┼───────────┤
│ Error Detection │    IP   │    TCP    │                        HTTP                       │   Wi─Fi   │
│ Error Tolerance │         │    UDP    │───────────┬──────────────┬────────────────────────┤  Ethernet │
│                 │         │           │   Socket  │     ASCII    │                        │           │
│                 │         │           │           │     UTF─8    │                        │           │
│                 │         │           ├───────────┼──────────────┘                        │           │
│                 │         │           │           │                   FTP                 │           │
│                 │         │           └───────────┴──────────────┬────────────────────────┴───────────┤
│                 │         │                 TLS                  │                                    │
└─────────────────┴─────────┴──────────────────────────────────────┴────────────────────────────────────┘
```

## HTTP

```text
POST / HTTP/1.1
Host: www.example.com
Content-Type: application/json
Content-Length: 15

{"name":"evan.lu"}
```

空行後的下一行即為代表本次*請求*的 **body**，範例中的 **body** 是常見的 `JSON` 格式。

由此，可以想像 `JSON` 格式是在*應用層*之上的**第八層**。

### JSON

單純透過 `JSON` 傳遞有什麼缺點？

1. 正確的資料格式應該要長什麼樣子？
2. 使用者需要閱讀相關文件，有辦法讓機器自動處理嗎？

為了解決上述問題，就會有其他 protocol 需要被引入。

不過除了用其他協定，也有一些方式可以舒緩（降低）上述發生的問題，如：

- [JSON API](https://jsonapi.org/format/)
- [JSON Schema](http://json-schema.org/specification.html)
- [OpenAPI (Swagger)](https://swagger.io/specification/)

> 上述僅是制定一些規範，讓使用者在閱讀相關 API 文件時，能較快進入狀況。

### GraphQL

GraphQL 讓*使用者*在跟*服務*要取資料的時候能指定特定資料，這有幾個好處：

- 可以拿到最準確的資料，減少網路傳輸
- 把多種服務的資料在一次請求中要齊

這也讓 GraphQL 通常成為 _facade services_，也就是在眾多服務中的首個接觸點，並作為對外溝通的唯一渠道。

> GraphQL 並不限定在要 HTTP 上執行，也能執行如 TCP 等協定之上。

> 雖然請求時送出的是類似 Query 的語法，但 Response 並無指定，只要能代表其階層式的結果就行，如 `JSON`。

#### 規範

```graphql=
type RecipeRoot {
  recipe(id: ID): Recipe
  pid: Int
}
type Recipe {
  id: ID!
  name: String!
  steps: String
  ingredients: [Ingredient]!
}
type Ingredient {
  id: ID!
  name: String!
  quantity: String
}
```

這份檔案是可以對外公開的，幫助使用者依此撰寫程式，類似上述提到的 OpenAPI。

#### 請求

這時，我們可以依照上述的規範送出請求：

```
{
  pid
}
```

```json=
{
  "data": {
    "pid": 9372
  }
}
```

```
{
  recipe(id: 42) {
    name
    ingredients {
      name
      quantity
    }
  }
}
```

```json=
{
  "data": {
    "recipe": {
      "name": "Chicken Tikka Masala",
      "ingredients": [
        { "name": "Chicken", "quantity": "1 lb" },
        { "name": "Sauce", "quantity": "2 cups" }
      ]
    }
  }
}
```

---

#### Code Demo

下列則是以 Node.js 為基礎的範例：

- [web-api 原始碼](https://github.com/evan361425/distributed-node/blob/master/src/web-api/consumer-graphql.ts)

```typescript=
// 僅展示請求的範例，這裡的 `kitchenSink` 是自定義名稱，方便 debug 用的
const query = `query kitchenSink ($id:ID) {
  recipe(id: $id) {
    id name
    ingredients {
      name quantity
    }
  }
  pid
}`;
const variables = { id: '42' };

return got(`http://${TARGET}/graphql`, {
  method: 'POST',
  json: { query, variables },
})
```

- [recipe-api 原始碼](https://github.com/evan361425/distributed-node/blob/master/src/recipe-api/producer-graphql.ts)

```typescript=
import { GraphQLID, GraphQLInt, GraphQLObjectType, GraphQLSchema } from 'graphql';

// 僅展示 RecipeRoot 的建置方式
const recipeRoot = new GraphQLObjectType({
  name: 'RecipeRoot',
  fields: {
    pid: {
      type: GraphQLInt,
      resolve: resolvers.RecipeRoot.pid,
    },
    recipe: {
      type: recipeQuery,
      args: { id: { type: GraphQLID } },
      resolve: resolvers.RecipeRoot.recipe,
    },
  },
});
return new GraphQLSchema({ query: rootQuery });
```

#### Live Demo

http://localhost:4000/graphql

### gRPC

像是 REST 或 GraphQL 都是建立在資料之上，而透過 CRUD 的方式去執行行為，這裡就可以注意到其限制：

> 大量的名詞，而僅有少量的動詞

舉例：
若有一個 API endpoint 是用來建立發票，今欲新增一附帶條件：**是否同時寄送信箱通知**。
有什麼樣的方式？

- 再建立一個 endpoint 專門做這件事： 過多 API，難管理和理解
- 在該 endpoint 新增變數：`need_send_email`： 讓該 endpoint 越來越複雜

`Remote Procedure Call` 就是來解決此事的！

> gRPC 為 Google 建立的 RPC 標準

gRPC 預設即非使用 JSON 格式進行資訊的傳遞，而是以 `Protocol Buffers`（ProtoBufs）的方式進行傳遞。

有幾個條件：

- 所有格式皆須預先設定好，副檔名為 `.proto`，且需要讓 client 擁有。
- 各值需給定順序，且之後不建議修改。
- 數字有多型別：`int32`，`int64`，`float`，`double` 等等。

這些條件有幾個好處：

- 效能、體積的最優化，binary serialize/deserialize

```text
{"id":42} v.s. 42
```

- 向後相容

```text
v1 需要 arg1 arg2
v2 需要 arg1 arg2 arg3
若 client 僅拿到 v1 的 proto，程式上會自動忽略 arg2 後的參數
```

---

#### Code Demo

- gRPC proto

```proto=
syntax = "proto3";
package recipe;
service RecipeService {
  rpc GetRecipe(RecipeRequest) returns (Recipe) {}
  rpc GetMetaData(Empty) returns (Meta) {}
}
message Recipe {
  int32 id = 1;
  string name = 2;
  string steps = 3;
  repeated Ingredient ingredients = 4;
}
message Ingredient {
  int32 id = 1;
  string name = 2;
  string quantity = 3;
}
message RecipeRequest {
  int32 id = 1;
}
message Meta {
  int32 pid = 2;
}
message Empty {}
```

- 建立 service，[原始碼](https://github.com/evan361425/distributed-node/blob/master/src/recipe-api/producer-grpc.ts)

```javascript=
import { loadPackageDefinition, Server } from '@grpc/grpc-js';
import { loadSync } from '@grpc/proto-loader';

// 讀取 proto 檔
const def = loadSync(__dirname + '/grpc.proto');
const proto = loadPackageDefinition(def);

// 建立處理邏輯
// handlers = ...;
const server = new Server();
server.addService(
  proto.recipe.RecipeService.service,
  handlers,
);

// 建立對外連線
// credentials = ...; for https
const cb = () => server.start();
server.bindAsync(`${HOST}:${PORT}`, credentials, cb);

// 建立 handlers
const handlers = {
  GetMetaData: (_call, cb) => {
    cb(null, { // error = null
      pid: process.pid,
    });
  },
  GetRecipe: (call, cb) => ({}) // if (call.request.id === 42)
}
```

- 建立 client，[原始碼](https://github.com/evan361425/distributed-node/blob/master/src/web-api/consumer-grpc.ts)

```javascript=
import { loadPackageDefinition } from '@grpc/grpc-js';
import { loadSync } from '@grpc/proto-loader';

// 讀取 proto 檔
const def = loadSync(__dirname + '/grpc.proto');
const proto = loadPackageDefinition(def);

// credentials = ...; for https
const client = new proto.recipe.RecipeService(TARGET, credentials);

client.getMetaData({}, cb);
client.getRecipe({ id: 42 }, cb);

```

#### Live Demo

http://localhost:3001

---

## Alternatives

除了 gRPC 還有什麼類似的東西？

**ProtoBufs**

_MessagePack_

雖然同為 binary representation of hierarchical object data，但

- 有 field
- 不需要額外檔案（如 `.proto`）去描述

**gRPC**

- _Apache Thrift_
- _JSON RPC_

關於 gRPC 推薦的文章：

- [比較 gRPC 服務與 HTTP API](https://docs.microsoft.com/zh-tw/aspnet/core/grpc/comparison?view=aspnetcore-5.0)

## 結論

1. JSON
   你需要一個 http client 來呼叫眾多 API Endpoint，訊息格式也需要有額外的 Schema 定義
2. GraphQL
   你還是需要一個 http client，但是這次只需要對應一個端點，而且可以自己組織查詢內容
3. gRPC
   你連 http client 都不用，套件會幫你產出這些呼叫的程式邏輯，而你只需要像寫一般 function 一樣呼叫即可
