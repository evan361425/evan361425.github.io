# Retry 的策略

## Retry in HTTP method

| Method | Idempotent | Destructive | Safe | 4XX      | 5XX      | Ambiguous | Purpose        |
| ------ | ---------- | ----------- | ---- | -------- | -------- | --------- | -------------- |
| GET    | O          | X           | O    | No Retry | Retry    | Retry     | 取得資料       |
| POST   | X          | X           | X    | No Retry | No Retry | No Retry  | 建立資料       |
| PUT    | O          | O           | X    | No Retry | Retry    | Retry     | 建立或編輯資料 |
| PATCH  | X          | O           | X    | No Retry | Retry    | Retry     | 編輯資料       |
| DELETE | O          | O           | X    | No Retry | Retry    | Retry     | 刪除資料       |

!!! info "Idempotent"

    冪等的，重複執行後結果仍相同

!!! info "Destructive："

    破壞性的，執行後會可能會造成資料的無法復原

PUT 可能為 `user.name = 'Evan'`，PATH 可能為 `user.access_count += 1`，故冪等是不同的。

若為 Destructive，可使用 `ETAG` 和 `If-Match` 的 HTTP 表頭來確認是否重複修改，或在更改過程中，從他處已經被修改。

> 就如同 Memcached 的 `CAS` 值

> 每次 Request 中增加 idempotency key 可以用作 cache key

## Circuit Breaker Pattern

多久 Retry 一次？

-   網路斷線，可能僅造成數毫秒的 rejection
-   DB connection，可能造成數秒的 rejection
-   reboot 可能造成數分鐘的 rejection
-   rolling back 可能造成小時的 rejection

在上述的情況下，exponential backoff 就是業界的 retry 標準，例如：

-   100ms
-   250ms
-   500ms
-   1s
-   2.5s
-   5s
-   5s
-   ...
-   quit

### Jitter

若同時有許多 instance 要 retry connection，可能會導致同時間過多的 request 進入 server 中。

![](https://i.imgur.com/kBdS63z.png)

如上圖所示，這狀況就叫 `thundering herd`。

這時在各個 instance 中增加 ±10% 內的亂數會平均分散這些請求。這種做法就叫做 `jitter`

```javascript
let time = SCHEDULE[times] || DEFAULT;
return Math.random() * (time * 0.2) + time * 0.9;
```

或是增加 offset：

```javascript
const PERIOD = 60_000;
const OFFSET = Math.random() * PERIOD;
setTimeout(() => {
    setInterval(() => retry(), PERIOD);
}, OFFSET);
```
