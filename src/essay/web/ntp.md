# NTP

[Network Time Protocol](http://en.wikipedia.org/wiki/Network_Time_Protocol)
說明如何讓各方裝置可以和中央的 NTP Server 進行校時的工作。

## 運作原理

![NTP 運作原理](https://i.imgur.com/vx3MZ2B.png)

NTP 是透過計算來回的時間差來得知節點和中原標準時間的差異，
要注意的是 NTP 在校時的時候是一次動一點然後逐漸靠近到正確時間（每秒 0.5ms）。

但是會有些問題：

- 若相差過大（系統大部分都是預設 128ms），則會暫停同步並強制重設；
- 去回的網路延遲差異過大會大幅降低校時的精準度；
- [閏秒](#閏秒)問題；
- VM 的石英震盪器是虛擬的，也就是會受到 CPU 影響，而降低準確性
- NTP Server 的[錯誤設定](https://blog.rapid7.com/2014/03/14/synchronizing-clocks-in-a-cassandra-cluster-pt-1-the-problem/)；
- 防火牆擋住和 NTP 的連線。

另外 NTP 是基於阜口 123 的 UDP 進行傳輸。

## 演進

| Version | Year | RFC | Desc. |
| - | - | - | - |
| v0 | 1981 | RFC 958 | NTP 概念首次提出，定義準確度、預估可能的誤差和[相對時鐘](../../feedback/designing-data-intensive-applications/distributed-env.md)的特性 |
| v1 | 1988 | RFC 1059 | 提出實作規則、相關演算法和 client-server 與 peer-to-peer 的模式 |
| v2 | 1989 | RFC 1119 | 提供驗證和控制訊息 |
| v3 | 1992 | RFC 1305 | 校時機制、上游時鐘的選擇和過濾演算法並支援廣播時間資訊，被廣泛使用的版本 |
| v4 | 2010 | RFC 5905 | 支援 IPv6 和提供加密和驗證手段來強化安全性 |

> NTP 演進

參考 [Info-Finder](https://info.support.huawei.com/info-finder/encyclopedia/en/NTP.html)。

## 閏秒

由於 UTC 時間透過原子鐘做計算，以此可以精準得出過了多少時間，但是和一般使用的曆法會有所衝突。

衝突就來自於一般曆法是透過觀測太陽來設計出一整年有 365.25 天。但實際地球自轉和公轉的週期是有些微變化的，也就是，透過原子鐘計算的時間會和曆法時間會有不規則的差異。

!!! quote "不規則性"

    地球自轉速度減慢的主要原因是[潮汐摩擦](../../feedback/future-of-fusion-energy/energy.md#潮汐)，
    僅此一項就將使一天每世紀延長 2.3ms。
    其他促成因素包括地球地殼相對於其核心的運動，
    地函對流的變化，以及導致巨大質量再分配的任何其他事件或過程。
    
    這些過程改變了地球的慣性矩，由於角動量守恆而影響了自轉速率。
    其中一些重分配會提高地球的自轉速度，縮短太陽日，並對抗潮汐摩擦。
    例如，冰河反彈將太陽日縮短了 0.6ms / 世紀，
    2004 年發生在印度洋的地震和海嘯被認為縮短了 2.68 微秒。

為了消彌這項差異，閏秒被設計出來了。

!!! info "閏秒可加可減"

    閏秒會被加進原子鐘算出的 UTC 時間，理論上可以是增加或減少。
    但歷史上（自從 1972 年以後）只增加過閏秒。

### 抹黑在閏秒附近的時間

「抹黑在閏秒附近的時間」是維基百科的翻譯，英文為 **leap smear**。這是 [Google 提出的](https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html)技術，主要為了避免使用傳統方式會造成的系統錯誤。

傳統方式是在 0 點前的那一秒多等待一秒，也就是那一秒會需要兩秒的時間來完成，這個機制會在許多的地方出現錯誤判定，尤其是依賴時間的系統，甚至影響應用程式的判斷。Leap smear 就是把這一秒隨機分散給當天的每一秒，讓被分配到的秒要跑久一點點，讓系統幾乎感受不到今天多了一秒。

## 廢除

最近（2022/08）有聽到要廢除閏秒的風聲，例如 Meta（以前稱 Facebook）工程在 [It’s time to leave the leap second in the past](https://engineering.fb.com/2022/07/25/production-engineering/its-time-to-leave-the-leap-second-in-the-past/) 提到的，未來的一千年（millennium）若忽略閏秒的影響，仍然能平衡電腦時間和曆法時間的差異而忽略其帶來的影響，至少機率上來說是如此。

已經經過[決議](https://www.nature.com/articles/d41586-022-03783-5)（2022/11/18）確定廢除閏秒了，並將於 2035 年後開始實施。
原因是目前地球自轉正加速中（每天的秒數將減少，儘管理論上應該受到月球引力而減慢），所以長遠來看，歷來只增加過的閏秒將會被平衡。

## Referrer

1. [Time, technology and leaping seconds](https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html)
2. [The One-second War](https://queue.acm.org/detail.cfm?id=1967009)

<!-- prettier-ignore-start -->
*[閏秒]: Leap Second
<!-- prettier-ignore-end -->
