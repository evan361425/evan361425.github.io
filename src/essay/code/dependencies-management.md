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
Gordon Bell 也說過：
[The cheapest, fastest and most reliable components of a computer system are those that aren't there.](https://dl.acm.org/doi/10.1145/4284.315122)。
安裝依賴需要耗的功有可能會大於直接維護需要的工具邏輯。
在安裝前，需要到該工具的套件管理文件中確認他的依賴和複雜性，
他和應用程式的 code review 有相同的重要性，需要相同程度的審核。

除此之外也可以定期審視當前應用的依賴，做適當的縮減。

### 掃描依賴

掃描你最終的依賴圖（例如 [Open Source Insights](https://deps.dev/)），去真正了解你會使用的套件和版本。
除此之外，不要使用本地開發的依賴圖，而是最終交付到線上環境的依賴，例如 container 或 VM。

!!! info "YouTube 上的 Open source licenses"
    不知道大家有沒有看過 YouTube app 上列出的 open source licenses？
    它位於「個人化設定」＞「設定」＞「簡介」＞「開放原始碼授權」中，
    這也代表一個健康的產品是清楚知道自己用了什麼依賴的，儘管他可能是 transient dependency。

### 建立好依賴管理的策略

明確標示依賴的管理方式，例如版本定死，或者允許每次發布都選擇最新版本的工具。
各有優缺點，重要的是確保共同開發者遵守這項規範（落成文件）。

### 發布清楚的屬性

屬性清單並不是 SBOM，而是清楚的作者資訊、提交 bug 的方式、license 和被共同編譯的依賴等，
可以幫助工具使用者操作的資訊。

但是現在很多套件管理對於作者資訊通常是非必要的，或許可以要求在註冊的時候設定 email 或 GitHub 帳號，
並在安裝工具時，提供這些資訊做溝通。

## 開源依賴的軟體供應鏈

前面提的是依賴管理的做法，這裡針對開源軟體供應鏈攻擊做[近一步的分析](https://queue.acm.org/detail.cfm?id=3722542)。
首先釐清幾個名詞，供應鏈攻擊（supply chain attack）、
供應鏈脆弱（supply chain vulnerability）
和供應鏈安全（supply chain security）。

- *供應鏈攻擊*是指在軟體交付前，將惡意的開源程式碼注入受信任軟體中的行為。（此定義改編自 Kim Zetter）
- *供應鏈漏洞*是指受信任軟體中，由第三方開源元件所引入的可被利用的弱點，
  例如 [Log4j 的 bug](https://finance.yahoo.com/news/inside-race-fix-potentially-disastrous-234445533.html)
  和 Apple 的 [zero-click tackover](https://googleprojectzero.blogspot.com/2021/12/a-deep-dive-into-nso-zero-click.html)。
- *供應鏈安全*是針對開源軟體供應鏈攻擊與漏洞所進行的防禦工程。

首先這裡討論的是軟體供應鏈攻擊，而非[硬體供應鏈的攻擊](https://www.spiegel.de/international/world/the-nsa-uses-powerful-toolbox-in-effort-to-spy-on-global-networks-a-940969.html)
也不是[封閉軟體的供應鏈攻擊](https://dl.acm.org/doi/10.1145/3266291)。
（例如 2015 年，駭客在類似百度網盤的地方發布[假的 Xcode 安裝位置](https://unit42.paloaltonetworks.com/novel-malware-xcodeghost-modifies-xcode-infects-apple-ios-apps-and-hits-app-store/)，
使用這個假的 Xcode 編譯的軟體都會在執行時發送系統資訊給駭客。）

確保使用的開源軟體供應鏈機制是安全的，例如 Go 的 [checksum database](https://go.dev/design/25530-sumdb)，
每個發佈在 [pkg.go.dev](https://pkg.go.dev/) 的軟體都會被簽署，
並透過 hard code 在 Go 的公鑰來達到驗證。
除此之外，透過「信任第一次提交」的機制，讓這些簽署無法被異動（immutability）。
但這仍有個缺點，因為每次編譯後的服務可能會因為時間、依賴、使用者名稱等等外部因素影響最終打包的 checksum 值，
這樣就無法驗證該版本的 checksum 是否可以和 source code 重新編譯後的執行檔 match，
這稱為 [Reproducible Build](https://reproducible-builds.org/)，
而最近 Go 也[正準備開發相關功能](https://go.dev/blog/rebuild)。

## 總結

上面提到的手段和思辨是複雜的，也不應該讓各自團隊有自己一套規範，
更好的做法應是統一的管理，CI/CD 的一致性檢查，IDP (internal developer platform) 的直觀圖表展示等等。
這些機制的落實和維護是需要長期管理的，所以我自己推測小公司或新創公司可能不會急著做，
但是當公司久了，遇見各種鬼故事之後，就可能會開始有人思考著這些事。
