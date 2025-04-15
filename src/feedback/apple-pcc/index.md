---
tags: Apple
description: Apple 推出新的 LLM 基礎架構，嘗試消彌大家對雲端運算最忌諱的點：隱私性。
---

# Apple Private Cloud Computing

Apple 推出新的 Large Language Model (LLM) 基礎架構，嘗試消彌大家對雲端運算最忌諱的點：隱私性。
這個架構被稱為私有雲計算，Private Cloud Computing (PCC)，本篇將細部討論其內部實作的邏輯。

異於官網的介紹方式，我們不在以技術細節為拆分，而是以系統目的來做拆分。
首先我們介紹 [PCC 的目標和信任基礎](./ability.md) 接著理解它[如何處理請求](handling.md)。

## 資料來源

- Apple 針對 PCC 的[官方說明文件](https://security.apple.com/documentation/private-cloud-compute/)
- [Apple wiki](https://theapplewiki.com/) 整理了很多 Apple 的技術細節。

--8<-- "abbreviations/apple-Intelligence.md"
