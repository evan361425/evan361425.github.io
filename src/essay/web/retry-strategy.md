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

    冪等的，重複執行後結果仍相同，例如重複刪除（delete）相同的資源，並不會造成額外的影響。

!!! info "Destructive："

    破壞性的，執行後會可能會造成資料的無法復原，之所以 POST 不是，是因為 POST 通常被用來建立資料，
    而不是修改資料。

_PUT_ 可能為 `user.name = 'Evan'`，
也可能為 `user.access_count += 1`，
故並不是每個操作都是 idempotent。

若為 destructive，可使用 [`ETag`](http.md#etag) 和 `If-Match` 的 HTTP 表頭來確認是否重複修改。

!!! note "CAS"
    就如同 Memcached/Redis 的 _CAS_（compare and set）。

## Circuit Breaker Pattern

多久 retry 一次？

- 網路斷線，可能僅造成數毫秒的 rejection
- DB connection，可能造成數秒的 rejection
- rolling back 可能造成數分鐘的 rejection
- reboot 可能造成數小時的 rejection

在上述的情況下，exponential backoff 就是業界的 retry 標準，例如：

- 100ms
- 250ms
- 500ms
- 1s
- 2.5s
- 5s
- 5s
- ...
- quit

### Jitter

若同時有許多 instance 要 retry connection，可能會導致同時間過多的 request 進入 server 中。

![當 server B 抖動時，所有請求都會同一時間進行重新傳送](https://i.imgur.com/kBdS63z.png)

如上圖所示，這狀況就叫 _thundering herd_，所有請求因為回傳，都擠在一起發送。

!!! example "相關實際案例"
    在 Google 分享的
    [Pokémon GO 事件](../../feedback/site-reliability-workbook/managing-load.md#案例研究pokémon-go)中，
    就是這個狀況的寫照。

這時在各個 instance 中增加 ±10% 內的亂數會平均分散這些請求。這種做法就叫做 _jitter_：

```javascript
function retryWaitSeconds(retryCount) {
    const time = SCHEDULE_WAIT_SECONDS[retryCount] || DEFAULT_WAIT_SECONDS;
    // return 0.9~1.1 time
    return Math.random() * (time * 0.2) + time * 0.9;
}
```

或是增加 offset：

```javascript
const PERIOD = 60_000;
const OFFSET = Math.random() * PERIOD;
setTimeout(() => {
    // 0~60 seconds
    setInterval(() => retry(), PERIOD);
}, OFFSET);
```
