# 維運上的一些心得

維運的核心思想是要**理解你的產品，並依據得到的數據作出決策**。

所謂的「理解產品」就帶代表透明化，log/metric/trace

log 又分三種：text log、introspection log（eg. exception stack） 和 structure log。

對於 SLO 來說 structure log 和 metrics 才是重點。

> 對於要找服務失能的問題，trace 和 text log 會是重點。
>
> Metrics 可能也包含這台主機上次部署時間（program version tag）。

SLO 可能是服務最久失能三十分鐘，SLI 會告訴你不同面向的指標，幫助你找到問題。

trace 要放 tcp 連線時間，可以幫助你快速釐清連線速度慢的原因。

> trace 跟 metrics 差在哪？
>
> -   trace 可以知道這個請求是每個連線都慢還是怎樣
> -   metrics 可以知道應用整體狀況

什麼都拉，例如 agent connections 從雲到地後變高，
agent log 看到 latency 拉高，對應調整，但是還沒做

照顧好你的 monitor 服務：

-   把設定變成 code，放近 VCS，加上 lint。
-   讓多團隊的 metrics 盡量一致。
-   獨立各個 component：
    -   collecting: `statsd`, `Prometheus`
    -   storing: `Prometheus`, `InfluxDB`(long term)
    -   dashboarding: `Grafana`, `Viceroy`
    -   alerting: `Alertmanager`

metrics 注意[四大指標](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)：

-   你的服務本身
-   你的依賴

但是要暴露這些資訊，你就會發現，我沒時間！這時候怎麼辦？

---

這就對到「我需要花多少時間在維運上」

再帶到 error budge，並依此導到「依據得到的數據做出決策」。

再依此導到公司架構，DevOps v.s. SRE

利用 THD 做一個範例。
