# 維運上的一些心得

維運的核心思想是要**理解你的產品，並依據得到的數據作出決策**。

理解產品代表：透明化，log/metric/trace

trace-> tcp 連線時間
跟 metrics 差在哪？
trace 可以知道這個請求是每個連線都慢還是怎樣
metrics 可以知道應用整體狀況

什麼都拉，例如 agent connections 從雲到地後變高，
agent log 看到 latency 拉高，對應調整，但是還沒做

這就對到「我需要花多少時間在維運上」

再帶到 error budge，並依此導到「依據得到的數據做出決策」。

再依此導到公司架構，DevOps v.s. SRE
