# 維運上的一些心得

維運的核心思想是要**理解你的產品，並依據得到的數據作出決策**。

所謂的「理解產品」就帶代表透明化，log/metric/trace

log 又分三種：text log、introspection log（eg. exception stack） 和 structure log。

對於 SLO 來說 structure log 和 metrics 才是重點。

> 對於要找服務失能的問題，trace 和 introspection log 會是重點。
>
> Metrics 可能也包含這台主機上次部署時間（program version tag）。

SLO 可能是服務最久失能三十分鐘，SLI 會告訴你不同面向的指標，幫助你找到問題。

trace 要放 tcp 連線時間，可以幫助你快速釐清連線速度慢的原因。

> trace 跟 metrics 差在哪？
>
> - trace 可以知道這個請求是每個連線都慢還是怎樣
> - metrics 可以知道應用整體狀況

什麼都拉，例如 agent connections 從雲到地後變高，
agent log 看到 latency 拉高，對應調整，但是還沒做

照顧好你的 monitor 服務：

- 把設定變成 code，放近 VCS，加上 lint。
- 讓多團隊的 metrics 盡量一致。
- 獨立各個 component：
  - collecting: `statsd`, `Prometheus`
  - storing: `Prometheus`, `InfluxDB`(long term)
  - dashboarding: `Grafana`, `Viceroy`
  - alerting: `Alertmanager`
- 定期讓某個服務壞掉或某個指標超過閥值，確保你的 alert 有通知到對的團隊
- 確保資料的即時性，才能在第一時間得到警訊

metrics 注意[四大指標](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)：

- 你的服務本身
- 你的依賴
- 總而言之，確保每個指標都有個目的

---

怎麼監控服務？假設你的 SLO 訂定 30 天最高 0.1% 的錯誤率：

- 讀取前十分鐘的資料檢查現在錯誤率是不是大於 0.1%。
    但實際上，這個十分鐘的「錯誤量」可能只佔 30 天的四千分之一，容易造成 False Alarm。
    換句話說，你可能可以每天收到 6*24 個警告，而仍能滿足你的 error budget
- 改成三十六小時的資料：
  - 三小時修復好的錯誤，會在接下來的三十三個小時一直叫
  - 耗費大量計算資源
- 改成每小時檢查一次，但會讓警告太晚收到

解法是：改成監控 burn rate，這個錯誤率會多快消耗掉你的 error budget：

- 假設認為每小時消耗掉 5% 的 error budget 是嚴重且需要告警的，就計算：
    burn rate 為 36（$\frac{30 day*24hr/day}{1hr}* 5\%$）。
    但仍會有問題：
  - burn rate 36 以下的錯誤就不會被告知，
        然而她只需約 20 小時就會把你的 error budget 吃掉。
        （低錯誤率而長期存在的漏洞）
  - 58 分鐘（$60 - 0.001*60*36$）的 reset time 仍太長
- 多等級的閥值：2/5/10% 的錯誤率、每 1/6/36 小時的資料、14.4/6/1 的 burn rate：
  - 缺點就是很多數值需要去參考、設定和說服
  - reset time 仍未減少
  - 可能一次觸發三個告警
- 搭配短時間的 AND 邏輯，例如：
  - 每小時 > 2%「且」每五分鐘 > 2%
  - 每六小時 > 5%「且」每三十分鐘 > 5%
  - 每三天 > 10%「且」每兩小時 > 10%

低流量的解法：

- 人工流量，但缺點：
  - 服務很複雜，偽造的流量通常只包含一部分的請求
  - 偽造的流量會讓真實的錯誤率下降
- 整合服務，把多個小的服務（擁有相似相依，例如資料庫）整合進大的監控系統，去計算 SLO
- 自動重新送出請求（retry），避免暫時性的錯誤影響使用者
- 降低 SLO 或拉長時間軸來做分析

有時太寬鬆的 SLO 會讓預期的告警失靈。
例如，SLO 每月 90% 以上的可用性，監控設定每小時 > 2% 的錯誤率將不可能被觸發：

\begin{align}
720*2\% = 14.4
rate >= 14.4* (1-90\%) = 1.4
\end{align}

要讓錯誤的請求大於請求總數的 1.4 倍，顯然是不可能的。

如果你有很多服務（微服務），不要每個都加上獨立的 SLO，而是把它分類好並套用其應有的 SLO。
例如：

| Request class | Availability | Latency @ 90%a | Latency @ 99% |
| - | - | - | - |
| `CRITICAL` | 99.99% | 100 ms | 200 ms |
| `HIGH_FAST` | 99.9% | 100 ms | 200 ms |
| `HIGH_SLOW` | 99.9% | 1,000 ms | 5,000 ms |
| `LOW` | 99% | None | None |
| `NO_SLO` | None | None | None |

---

但是要做這些東西，你就會發現，我的時間都被功能開發佔滿！這時候怎麼辦？

---

這就對到「我需要花多少時間在維運上」

再帶到 error budge，並依此導到「依據得到的數據做出決策」。

再依此導到公司架構，DevOps v.s. SRE

利用 THD 做一個範例。

> 公司有個案例，Java 過 GSLB 的連線池在 GSLB 的連線表被 reset，導致所有 db 連線失能。
