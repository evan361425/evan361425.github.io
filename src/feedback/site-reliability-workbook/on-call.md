---
tags: SRE-workbook
---

# 待命小組

SRE 的待命（on-call）和傳統的待命差異在於，比起專注於重複性的勞動，例如監聽錯誤事件、定期查看面板等等，
他們更專注於定義適當的閥值，優化開發流程和系統。

待命對線上服務的維運非常重要，且通常是個高緊張性的工作，不管是對個人或者團隊。
也因次設計一個系統化的待命機制是待命人員、待命小組、全公司都需要共同商討的議題。

> 如果你常常收到一些無關緊要的告警，我們建議你退後一步從更高的角度去觀察整個情況。
> 並且嘗試和其他夥伴或 SRE 團隊交換意見。

緊急情況的維運需要依靠 *平常練習帶來的肌肉記憶* 和 *完整文件幫助混亂狀況的指引*，這裡有幾個項目需要熟悉：

- [ ] 管理線上作業
- [ ] 理解日誌訊息
- [ ] draining 流量到另一個叢集
- [ ] rollback 錯誤的更新
- [ ] 阻擋或限制非預期的流量
- [ ] 增加節點，提高服務負載量
- [ ] 習慣監控面板
- [ ] 理解服務架構和服務的相依

要熟悉這些項目，就必須要做線上災難演練，如何製造災難，需要大家奇發異想。
每次執行 on-call 練習時，可以輪流當主席，包括災難的製造、告警和行動。

最後，非常重要的一點是，這些經驗要怎麼傳承，一份好的文件？一個好的搜尋平台？

把事件分類：

- P1，緊急事件、會通知 on-call、會開始執行事件的分類、影響 SLO；
- P2，影響範圍有限、會透過事件串流頻道告知；
- P3，被整合起來的訊息，通常和服務的容量有關。

這麼做的目的是把 on-call 從一些日常維運資訊中拉出來，只專注在緊急事件。

當有了 SLO，我們就可以每月進行公開的服務健康彙報，包括事件處理、錯誤預算等等，
讓那些股東能夠知道公司的服務健康狀況。
這種會議不只能夠傳達 SLO 的重要性，也讓開發者有個時間檢視自己的服務。

每次這些經驗，都會讓開發團隊有更容易跳出「事件分類、根因分析、事後析誤」的循環。
並進而強化和調整產品開發時的準則，最重改善 on-call 團隊的工作品質。

[PagerDuty](https://response.pagerduty.com/) 說明什麼是 [on-call](https://response.pagerduty.com/oncall/being_oncall/)
