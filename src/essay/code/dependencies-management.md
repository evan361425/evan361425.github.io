---
tags: Code
description: 開源軟體越來越豐富，但我們該如何管理好依賴？
---

# 依賴管理

世界上有很多人投入軟體開發，遇到類似問題時都會需要一些小工具來處理，
這些工具逐漸變成開源依賴，方便大家，不用重複造輪子，
但是隨著這些依賴增長，我們需要退一步來思考：該怎麼管理好這些依賴？

除此之外，前幾天看到一篇
「[why we no longer use LangChain for building our AI agents](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents)」，
過度依賴別人造好的輪子會讓逐漸膨脹的軟體漸漸失去彈性，
除了那些經歷過大量和長時間使用的框架（Express.js、FastAPI、Laravel），
很多新興工具是需要淬鍊來驗證其價值的。

## 建議做法

> 參照於：
> [The Surprise of Multiple Dependency Graphs](https://queue.acm.org/detail.cfm?id=3723000)

### 考量各依賴的成本

Go proverb 有這麼一句：
[A little copying is better than a little dependency.](https://www.youtube.com/watch?v=PAAkCSZUG1c)。
安裝依賴需要耗的功有可能會大於直接維護需要的工具邏輯。
在安裝前，需要到該工具的套件管理文件中確認他的依賴和複雜性，
他和應用程式的 code review 有相同的重要性，需要相同程度的審核。

除此之外也可以定期審視當前應用的依賴，做適當的縮減。

### 掃描依賴

掃描你最終的依賴圖，去真正了解你會使用的套件和版本。
除此之外，不要使用本地開發的依賴圖，而是最終交付到線上環境的依賴，例如 container 或 VM。

### 建立好依賴管理的策略

明確標示依賴的管理方式，例如版本定死，或者允許每次發布都選擇最新版本的工具。
各有優缺點，重要的是確保共同開發者遵守這項規範（落成文件）。

### 發布清楚的屬性

屬性清單並不是 SBOM，而是清楚的作者資訊、提交 bug 的方式、license 和被共同編譯的依賴等，
可以幫助工具使用者操作的資訊。

但是現在很多套件管理對於作者資訊通常是非必要的，或許可以要求在註冊的時候設定 email 或 GitHub 帳號，
並在安裝工具時，提供這些資訊做溝通。
