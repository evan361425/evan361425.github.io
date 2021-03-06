# NTP

[Network Time Protocol](http://en.wikipedia.org/wiki/Network_Time_Protocol) 說明如何讓各方裝置可以和中央的 NTP Server 進行校時的工作。

## 運作原理

![NTP 運作原理](https://i.imgur.com/vx3MZ2B.png)

NTP 是透過計算來回的時間差來得知節點和中原標準時間的差異，要注意的是 NTP 在校時的時候是一次動一點然後逐漸靠近到正確時間。

但是會有些問題：

-   若相差過大，則會暫停同步並強制重設
-   去回的網路延遲差異過大會大幅降低校時的精準度
-   [閏秒](#_1)問題
-   VM 的石英震盪器是虛擬的，也就是會受到 CPU 影響，而降低準確性
-   NTP Server 的[錯誤設定](https://blog.rapid7.com/2014/03/14/synchronizing-clocks-in-a-cassandra-cluster-pt-1-the-problem/)
-   防火牆擋住和 NTP 的連線

## 閏秒

由於 UTC 時間透過原子鐘做計算，以此可以精準得出過了多少時間，但是和一般使用的曆法會有所衝突。

衝突就來自於一般曆法是透過觀測太陽來設計出一整年有 365.25 天。但實際地球自轉和公轉的週期是有些微變化的，也就是，透過原子鐘計算的時間會和曆法時間會有不規則的差異。

!!! quote "不規則性"

    地球自轉速度減慢的主要原因是潮汐摩擦，僅此一項就將使一天每世紀延長 2.3ms。其他促成因素包括地球地殼相對於其核心的運動，地函對流的變化，以及導致巨大質量再分配的任何其他事件或過程。這些過程改變了地球的慣性矩，由於角動量守恆而影響了自轉速率。其中一些重分配會提高地球的自轉速度，縮短太陽日，並對抗潮汐摩擦。例如，冰河反彈將太陽日縮短了 0.6ms / 世紀，2004 年發生在印度洋的地震和海嘯被認為縮短了 2.68 微秒。

為了消彌這項差異，閏秒被設計出來了。

!!! info "閏秒可加可減"

    閏秒會被加進原子鐘算出的 UTC 時間，理論上可以是增加或減少。
    但歷史上（自從 1972 年以後）只增加過閏秒。

### 抹黑在閏秒附近的時間

「抹黑在閏秒附近的時間」是維基百科的翻譯，英文為 **leap smear**。

## Referrer

1. [Time, technology and leaping seconds](https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html)
2. [The One-second War](https://queue.acm.org/detail.cfm?id=1967009)

<!-- prettier-ignore-start -->
*[閏秒]: Leap Second
<!-- prettier-ignore-end -->
