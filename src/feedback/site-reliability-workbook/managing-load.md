---
tags: SRE-workbook
---

# 負載管理

負載平衡（load balancing）、負載削減（load shedding）和自動擴增（auto scaling），
這些機制都可以幫助改善服務的負載狀況，通常一個大型服務的負載管理機制包含這上述三種方式。
但是這些機制都需要同步彼此的狀態，否則很可能在某些時候造成錯誤（自動化的）設置，並破壞可用性。

在這些千奇百怪的狀況中，本章節提供一些建議來遵循。

## Google Cloud Load Balancing
