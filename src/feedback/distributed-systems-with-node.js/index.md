# Distributed Systems with Node.js

| 參考書籍                           | 使用 Repo                     |
| ---------------------------------- | ----------------------------- |
| [Distributed-Systems-with-Node.js] | [evan361425/distributed-node] |

![Distributed Systems with Node.js](https://i.imgur.com/UeShSDB.png)

## 說明

傳統上，應用程式皆為同一包程式碼中，這時會造成什麼問題？

1. 修改程式碼時，可能無意間破壞掉其中各個關係的協作，Debug 代價很高
2. 每次交付、部署都會花很長時間
3. 新進員工，或想進入這個專案的門檻（理解專案的時間）提高

整體來說，這樣的做法成本太高了。

---

分散式系統，即是把一個大型應用程式，拆成幾個小的服務。
這時仍會遇到傳統做法不會遇到的問題：

1. 風險提高，因服務彼此之間有連結，若 A 服務壞了，B 服務也會壞掉。多一台機器，就多一份機器壞掉的風險
2. 增加溝通需要的時間、風險和流量
3. 本來同一個應用程式，可以共用一份設定檔、程式碼和機敏資料，若服務變多了，該怎麼同步這些共用的檔案
4. 要怎麼知道特定 Request 為什麼會回 500，哪台壞了？
5. 限制特定服務僅能在服務間溝通，而不能對外（VPC）

---

之後會使用的範例架構若無說明則為：

![範例基礎架構](https://i.imgur.com/wNBnrOA.png)

講解順序：

（後面的「問題 x」代表嘗試解決的問題）

1. [Protocol](./protocol.md) - 不同的服務間，該用什麼方式溝通，問題 2
2. [SLA and Load Testing](./sla-and-load-testing.md) - 如何證明效率在接受範圍內，問題 2
3. [Observability](./observability.md) - Log、Metric 和 Tracing，問題 4
4. [Container](./container.md) - 服務變多了，部署上該使用什麼方式，問題 1
5. [Container Orchestration and Misc.](./container-orchestration-and-misc.md) - 容器調度工具，問題 1~5

[distributed-systems-with-node.js]: https://www.booktopia.com.au/distributed-systems-with-node-js-thomas-hunter-ii/ebook/9781492077244.html
[evan361425/distributed-node]: https://github.com/evan361425/distributed-node
