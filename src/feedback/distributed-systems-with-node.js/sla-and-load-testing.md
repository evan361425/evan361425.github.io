# SLA and Load Testing

## 說明

產品都需要向使用者展示部分的**承諾**，例如：

-   要求在 100ms 內回應（Latency）
-   1 年當中僅有 1 小時以內的時間服務可能無法使用
-   任何變動都會保證一年內的向後相容

這類保證，稱為 SLA（Service Level Agreement）。

> SLA 通常由多個 SLO（Service Level Objective）組成，例如：
> 一份 SLA 提供 `快速且安全的支付金錢`，其中的 `保證不會重複扣款`即為 SLO
>
> SLI（Service Level Indicator）即是 SLO 的指標，例如
> 目標在 100ms 內回應，實際測試為平均於 80ms 內回應

好的服務 `SLO / SLI` 需大於等於 `1`。

### 分散式系統中的意義

若要求在一個服務有特定的 SLO，就必須同時計算該服務中所有會使用的子服務的 SLO。

![一個服務的 SLo 代表著所有子應用執行的總時間](https://i.imgur.com/iutCl8W.png)

> 有時候，產品過於複雜沒辦法產出完整的流程圖，事實的簡化或增加 Tracing 都可以幫助產出。

---

## Load Test

Load Test 目的即是計算出 SLI。

> Load Test 和 Stress Test 差在哪裡？

Latency 代表從`事件觸發`到`事件回應`的時間差，此處並不包含錯誤回應的狀況。

> 以下範例，都將以 Latency 為 SLO，並計算之。

---

## Baseline

測試重要的一點是要有一個基準點，一個產品可以有多種 Baseline

例如：

-   在不做任何外部請求之下的 Latency
-   使用的框架所限制的 Latency

> 不同的 Baseline 會有自己的意義，根據需求制定出理想的 Baseline。

### 範例

以 Node.js 這語言所能做出最單純的 server 為 Baseline：

```javascript
require("http")
    .createServer((req, res) => res.end("ok"))
    .listen(80, () => null);
```

依此觀察出，在統一機器規格下任何要求在 Node.js 這語言有超越其 Latency 都是沒意義的。

> 在追求更好的 Latency 時，或許該考慮其他語言，如 C++ 或 Rust。
> 但此時便需要權衡其他考量，如：會使用該語言的人數，社群發展程度等等。

### Latency

| Stat    | 2.5%   | 50%    | 97.5%  | 99%    | Avg       | Stdev    | Max    |
| ------- | ------ | ------ | ------ | ------ | --------- | -------- | ------ |
| Latency | 0ms    | 0ms    | 0ms    | 0ms    | 0.01ms    | 0.08ms   | 9.45ms |
| Req/Sec | 42,751 | 39,039 | 36,703 | 29,487 | 38,884.14 | 1,748.17 | 29,477 |

![Latency 的長尾分佈](https://i.imgur.com/sDcMyqC.png)

其中的 `29487 個每秒請求量`即是 TP99（Top Percentile）下的基準點。

> 有時會認為 1% 是極端值，應該忽略。然而在網路世界中，一個使用者常常會需要針對一個網頁做出很多請求。若以一個頁面需要 40 個資源來計算，在跑第五個頁面之後，有近乎 0.003 % 的機率使用者 **不會** 觸發到 95% 的狀況。
> [How NOT to Measure Latency](https://www.youtube.com/watch?v=lJ8ydIuPFeU)

## 使用 Reverse Proxy - HAProxy

| Percentile | With Proxy | Without |
| ---------- | ---------- | ------- |
| 99.9%      | 1ms        | 1ms     |
| 99.99%     | 2ms        | 2ms     |
| 99.999%    | 5ms        | 3ms     |

得到 `19967 個每秒請求量`，相比於基準點 `29487`，看得出在最單純的應用程式下增加 r-proxy 會讓應用程式變慢。

但若考慮真正的應用程式，假如回應時間為 100ms，使用 r-proxy 雖會增加回應時間，卻僅僅增加 1~2ms，整體效益還是大於其消耗的效能。

## 若考慮 HTTP Compression

上述例子僅考慮最基礎的框架效能，若為了壓縮網路流量

-   套用 compression，對於效能會有什麼影響？
-   再加上 r-prxoy 又會有什麼影響？

### Latency

| Percentile | With Proxy | Without |
| ---------- | ---------- | ------- |
| 99%        | 47ms       | 53ms    |
| 99.9%      | 50ms       | 57ms    |
| 99.99%     | 52ms       | 62ms    |
| 99.999%    | 53ms       | 64ms    |

## Protocol

上一份報告討論各種服務間的溝通方式：

-   JSON over HTTP
-   GraphQL
-   gRPC

究竟哪一項是真正有效率的？

### 結果

| Percentile | JSON | GraphQL | gRPC |
| ---------- | ---- | ------- | ---- |
| 99%        | 10ms | 13ms    | 24ms |
| 99.9%      | 18ms | 22ms    | 32ms |
| 99.99%     | 26ms | 36ms    | 82ms |
| 99.999%    | 48ms | 67ms    | 82ms |

### 討論

我們知道 GraphQL 的價值在於可以在一個 request 中取得所有訊息，且不需要針對每個場景對外開出一個 endpoint。

有時為了追求開發效率，而會捨棄部分產品效率，這時便要權衡產品的特性較偏向於哪邊。

除此之外 JSON 的解析在 v8 engine 中，效率已經被極致的壓縮了，所以相對而言，利用 Buffer 做 binary 解析的 gRPC 在效能上就矮了一截。由於其特性，讓他在 C++ 這類編譯過的程式碼中有較高的效能，而不額外處理 GC 這類事件。

## 結論

1. SLA 是面向很多的指標，有時必須權衡
2. 正確的評估符合自己的指標，例如：自動填寫 vs 銀行開戶
3. 在做 load testing 時，需要注意產品可能的流量高低峰
4. 要盡量減少雜音（noisy neighbor），盡量在類似線上的環境中測試
5. 一個產品究竟該開幾個（多少 CPU/Memory）機器來滿足線上流量？

### 方向

1. 觀察線上環境現有的流量高峰，並制定出符合商務邏輯的 Latency（SLO）。
2. 制定單位：一個 Docker container、一台機器、EC2
3. 找出在滿足 TP99 下的請求數
4. 增加單位，反覆測試直到達到能容納線上環境的數量

#### 範例

若希望產品能在 50ms 內回應請求，並得出線上環境高峰約每秒 20 （或每分 1200 或每時 72000）個請求。

啟用一個 Docker container 時，如要在 TP99 內回應 50ms 以下，僅能接受每秒 6 個請求。

再增加一個 Docker container，此時能接受每秒 10 個，依序往下加。
最終得到 4 個 container 為合理數量。

### 工具

上述所有測試，皆是使用 [autocannon](https://github.com/mcollina/autocannon) 這軟體測試，相關代碼模式皆為：

```bash
autocannon -d 60 -c 10 -l http://localhost:3000
```

> 其意義在於：建立 10 個連線（`-c`），並持續（`-d`）60 秒，並展示詳盡的結果（`-l`），預設每個連線每秒打 1 次請求（`-p`）

對於該使用何種工具，其實不無特別要求，但是對於如何解讀結果，仍推薦 [How NOT to Measure Latency](https://youtu.be/lJ8ydIuPFeU?t=2042) 這部影片

若是多項服務合計的 latency（或甚至全公司），這時使用同一種工具就顯得重要了。

### 微實作

[auth](https://github.com/104corp/vip3-auth/tree/master/stress-test/2021-05)
