# 如何製作 Docker Container

建立 container 前，需要先建立 image，然而這步驟會和應用程式的需求而有很大的不同，在此謹概略介紹以 Node.js 為背景的應用程式。

製作 image 分為三個步驟：

1. 準備好應用程式的相依套件
2. 準備好執行應用程式的環境
3. 執行應用程式

## 準備好應用程式的相依套件

以 Node.js 為例，則是 `npm i` 或更精簡的 `npm ci --only=production`。
其他如：

- PHP 的 `composer install --no-dev --optimize-autoloader`
- Python 的 `pip install`
- Gradle 的 `bundle install --clean --without dev`

Dockerfile 是 Docker 用來建立 image 的指令表，類似 Makefile。
以下為 Node.js 建立相依套件的指令表：

```dockerfile
FROM node:lts-alpine AS deps

# Change current folder to /srv
WORKDIR /srv
COPY package*.json ./
RUN npm ci --only=production
```

上述每一行都代表一個 Layer，而每一次呼叫 `FROM`，即代表建立一組 Stage。

> 在 Docker 的 Best Practice 中會建議使用越少 command 越好就是避免過大的 layer

## 準備好執行應用程式的環境

在執行環境中，不需要一些 Node.js 的特定功能，如 `npm`。

```dockerfile
FROM node:lts-slim AS release
```

除此之外也可以在 Alpine 環境下建立極簡的 Node.js，詳見[實作的程式碼](https://github.com/evan361425/distributed-node/blob/master/Dockerfile-web)。

> 概念就是下載 `curl`（Alpine 無 `curl`）再下載 Node.js 後刪除不必要檔案

> 更完整內容詳見 Node.js 提供的建立 image 的[最佳做法指引](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

再來就剩把剛剛在 `deps` 環境中建立的相依套件拉過來：

```dockerfile
COPY --from=deps /srv/node_modules ./node_modules
COPY . .
```

警告：`COPY . .`代表會把現在本地端資料夾中的所有檔案複製此 image 中。
為了避免不必要檔案被複製，可於 `.dockerignore` 中設定

.dockerignore 範例：

```
node_modules
npm-debug.log
Dockerfile
.git
.gitignore
.eslintrc
```

## 執行應用程式

再來就剩準備設定檔和執行程式了：

```dockerfile
EXPOSE 1337
ENV HOST 0.0.0.0
ENV PORT 1337
CMD [ "node", "server.js"
```

## 包裝成 Container

```bash
docker build -t example/server:v0.0.1 .
```

這時就可以看到各個 layer 被執行的過程。

```
Sending build context to Docker daemon  155.6kB
Step 1/11 : FROM node:lts-alpine AS deps
 ---> 532fd65ecacd
... TRUNCATED ...
Step 11/11 : CMD [ "node", "server.js" ]
 ---> Running in d7bde6cfc4dc
Removing intermediate container d7bde6cfc4dc
 ---> a99750d85d81
Successfully built a99750d85d81
```

## 更新

Docker Image 在建立時，會透過 SHA 值進行暫存，所以當有部分改動的時候就不需要全部重新建立。

> SHA 值計算方式是上一個 SHA 值加上現行的指令組出來的。

也就是說，若改動的僅有應用程式的程式碼，如 `server.js`，在重建 image 時就僅需要執行 `COPY . .` 以後的代碼。

相對的，當 package.json 改變時（如 dependency 增加）就需要從 `deps` 這層 stage 開始建立起。

### 範例

透過 `docker history example/server:v0.0.1` 可以觀看其建立時的記憶體用量。

- `v0.0.1` 代表初始版本
- `v0.0.2` 代表修正 `server.js`
- `v0.0.3` 代表新增套件

| Layer                            | Size   | v0.0.1       | v0.0.2       | v0.0.3       |
| -------------------------------- | ------ | ------------ | ------------ | ------------ |
| 1: FROM node AS deps             | N/A    | 532fd65ecacd | 532fd65ecacd | 532fd65ecacd |
| 2: WORKDIR /srv                  | N/A    | bec6e0fc4a96 | bec6e0fc4a96 | bec6e0fc4a96 |
| 3: COPY package\*                | N/A    | 58341ced6003 | 58341ced6003 | 959c7f2c693b |
| 4: RUN npm ci                    | N/A    | dd6cd3c5a283 | dd6cd3c5a283 | 6e9065bacad0 |
| 5: FROM node:lts-slim AS release | 5.6MB  | e7d92cdc71fe | e7d92cdc71fe | e7d92cdc71fe |
| 6: COPY node_modules             | 67.8MB | a86f6f94fc75 | a86f6f94fc75 | b97b002f4734 |
| 7: COPY . .                      | 138kB  | cab24763e869 | 7f6f49f5bc16 | f2c9ac237a1c |
| 8: EXPOSE                        | 0      | 0efe3d9cd543 | 4fc6b68804c9 | f4b64a1c5e64 |
| 9: ENV HOST                      | 0      | 9104495370ba | df073bd1c682 | fee5ff92855c |
| 10: ENV PORT                     | 0      | 04d6b8f0afce | f67d0897cb11 | 638a7ff0c240 |
| 11: CMD                          | 0      | b3babfadde8e | 9b6514336e72 | 12d0c7e37935 |
| Cost per Deploy                  | N/A    | 0            | 138kB        | 68MB         |
