# 分散式系統的環境

本章會討論網路、時鐘、執行緒是如何影響 _分散式系統_ 的。

[HackMD 報告](https://hackmd.io/@Lu-Shueh-Chou/B1yGrqEy5)

我們有提過分散式的系統會讓單一資料庫中交易機制所能提供的一致性失去原有的保證。為了讓應用程式開發人員在分散式或者單台的資料庫都不會有太大的使用差異，我們需要個方法解決這問題。

不過在討論如何解決這問題之前，我們需要先來討論一下分散式的環境面臨了哪些困境，並讓我們對於整體環境有個初步的概念。

---

| 比較單台機器和分散式系統的差異~單台（HPC） | 分散式             |
| ------------------------------------------ | ------------------ |
| 全錯 or 正常                               | 部分錯且不正常運作 |
| 不容易出錯                                 | 容易出錯           |
| offline                                    | online—不允許停機  |
| 線路溝通                                   | 網路溝通           |
| checkpoint                                 | retry              |

單台高效能機器（High-Performance Computer, HPC）因為發生錯誤時通常是非常複雜的，可能牽涉到硬體、韌體、作業系統等等，為了讓發生錯誤時使用者仍然可以執行其他工作，執行工作的結果通常是要麻成功（得到預期的結果）要麻失敗（執行緒直接中斷）。

想像一下你在操作自己的筆電並執行操作（登入視窗、打開簡報）時，通常是要麻顯示執行成功要麻就是好像沒發生過任何事一樣，直接中斷程序。除此之外，當發生嚴重問題時作業系統很可能會讓系統重新啟動（藍螢幕、kernal panic 等等），而重新啟動之後原本的問題就神奇地消失了。

相對來說，分散式系統對於外部觀察者而言，當發生問題時會出現不預期的結果，例如明明顯示執行失敗，實際卻執行成功。而且明明沒做任何改變，重新執行第二次之後，又從失敗變成成功了。想想我們在維運時遇上的那些怪事！

接下來我們就會來說明一下，分散式系統到底處於什麼樣的環境讓他這麼異於單台機器。

> 不容易出錯通常代表當發生錯誤的時候，我們很可能是無能為力的。

> 這裡的錯誤都不考慮拜占庭錯誤。

## 簡介

![分散式系統的環境](https://i.imgur.com/1AYeXTG.png)

分散式系統雖然在相同成本下可以負荷更多的請求，也能避免過多的任一節點的中斷導致服務中斷。

我們都知道分散式系統的環境比單台機器的環境更不穩定，如圖上所示，他不僅需要面對執行緒的問題，更需要面對網際網路和不同時鐘的問題。

這時我們要問問自己，為什麼？為什麼明明在更不穩定的環境之中，卻能建立更高可用和更有效率的系統？

這是因為這些協定或者服務都是建立在每一子層（service, in OSI）的抽象維度之上。

一個 HTTP 請求是建立在

-   傳送二進位訊號的實體層
-   把二進位整合成訊框（frame）的資料連結層，以圖上為例就是 Ethernet 的交換器，並在這裡進行高容錯、偵錯的 CRC
-   利於大量擴展並管理多封包（packet）的網路層，以圖上為例就是 IP 的路由器
-   把這些包裝成網卡（NIC），並和 CPU 進行溝通
-   最後在軟體面上提供 UDP/TCP 等協定滿足各種資料的傳輸的傳輸層，以 TCP 為例，就會在此進行封包的排序、重新請求、消除重複等排除錯誤的行為
-   最後利用 BSD 提供的 API 讓應用程式得以和 OS 溝通，並完成這一系列的行為

每一層的抽象維度，讓你在和子層溝通時都完全不需要考慮更下層的機制，而最終拿到的應用程式資訊幾乎可以說是沒有任何錯誤的資訊。當然，你也可以在應用程式中，再做一次排錯的行為，例如當超過一定時間沒回應時，重新請求一次。

!!! info "好用資源"

    對於網際網路的運作，建議可以上 [Computer Communication](https://www.coursera.org/specializations/computer-communications?) 這一系列的課程。

    如果是要單單了解 OSI 不同層的意義和溝通的概略基礎介紹，可以上系列課程的第一堂課 [Fundamentals of Network Communication](https://www.coursera.org/learn/fundamentals-network-communications)

時鐘和執行緒的狀況也是一樣的！我們待會再細談，先繼續深入一下網際網路的問題。

## 網際網路

-   網路會遇到哪些問題？
-   要怎麼知道網路遇到哪些問題？
-   如何判定節點連不上了？
-   為什麼網路延遲是無界的？

順序會依序如上，但是當來到「要怎麼知道網路遇到哪些問題」時，會發現結果就是我們沒辦法知道發生什麼事。

既然無法知道網路遇到哪些問題，我們要怎麼判定特定節點連不上了？

通常是用逾時機制（Timeout），但是為什麼網路延遲是無界的（unbounded）？

> 我有寫了篇[網路怎麼傳](../../essay/web/network-routing.md)和[網路傳了什麼](../../essay/web/network-details.md)，有興趣了解更細的都可以查看。

### 有哪些問題

兩個方向：

-   **變因**，哪些是外在環境讓網路發生問題
-   **天生**，他的天生設計造成了什麼缺陷

#### 物理性損壞

![鯊魚咬海底電纜](https://compote.slate.com/images/87b79ce6-bb1c-42ca-ab42-9931a6284fe5.jpg?width=1600)

停電、地層下陷、喝醉的卡車司機等等。

> 圖片提供於[此文章](http://www.slate.com/blogs/future_tense/2014/08/15/shark_attacks_threaten_google_s_undersea_internet_cables_video.html)

!!! quote "Coda Hale 的經驗談"

    In my limited experience I’ve dealt with long-lived network partitions in a single data center (DC), PDU failures, switch failures, accidental power cycles of whole racks, whole-DC backbone failures, whole-DC power failures, and a hypoglycemic driver smashing his Ford pickup truck into a DC’s HVAC system. And I’m not even an ops guy.

#### 錯誤設定

![維基百科都有相關狀況的細部說明](https://i.imgur.com/conads1.png)

這個應該是主流。

1. [GitHub 因更新路由器時設置錯誤引發骨牌效應造成停機五小時](https://github.com/blog/1364-downtime-last-saturday)
2. [Facebook 因錯誤設定造成全球全服務六小時以上的停機](https://en.wikipedia.org/wiki/2021_Facebook_outage)
3. [Google 很少對外公布停機原因](https://en.wikipedia.org/wiki/Google_services_outages)

#### 韌體有錯

![在 Linux 提出的相關 bug issue](https://i.imgur.com/EpeBW6S.png)

單純軟體面有 bug：

-   [路由器單向無法送出](https://www.spinics.net/lists/netdev/msg210485.html)

如果想了解更多可能會有的問題，可以查閱：

-   https://queue.acm.org/detail.cfm?id=2655736
-   https://queue.acm.org/detail.cfm?id=2482856

### 如何知道正發生哪些問題

![沒得到回應時，問題可能發生任何地方](https://i.imgur.com/F5cbLAa.png)

要怎麼知道網路遇到哪些問題？

網際網路的問題發生在任何地方，過去或回來的路上。而問題可能是延遲、錯誤、遺失。

你沒有辦法透過單一一個錯誤請求知道是哪種原因造成這個錯誤請求。

既然無法知道網路遇到哪些問題，我們要怎麼判定特定節點連不上了？

### 如何判定節點下線了

有一些方法

-   當目的端的阜沒開，[TCP 會回應 `FIN` 或 `RST`](http://blog.netherlabs.nl/articles/2009/01/18/the-ultimate-so_linger-page-or-why-is-my-tcp-not-reliable)
    -   當目的節點正面臨網路壅塞，[TCP 會回應一些警告資訊](https://notfalse.net/28/tcp-congestion-control#-Congestion-Avoidance)
-   若應用程式中斷，但是 OS 仍在執行，有些[資料庫](http://blog.thislongrun.com/2015/05/CAP-theorem-partition-timeout-zookeeper.html)會有機制告訴叢集內的資料庫：「我無法運作了！」
-   可以監控交換器（switch）、路由器（router）甚至中繼器（repeater）的管理系統
    -   若對這些名詞不了解，推薦[這篇](https://notfalse.net/66/repeater-hub-bridge-switch)中文文章，不過若要更有系統地了解還是建議 coursera 課程
-   有些路由器會回封包（[ICMP Destination Unreachable](http://www.tsnien.idv.tw/Network_WebBook/chap13/13-5%20ICMP%20通訊協定.html)）告訴你該節點是無法連線的
-   Timeout（[TCP 本身就有](https://ms2008.github.io/2017/04/14/tcp-timeout/)，此指應用程式面），靠經驗決定應該在多長時間內回應
    -   [Phi Accrual](https://doc.akka.io/docs/akka/current/typed/failure-detector.html) 動態調整 Timeout 時間
    -   [抖動緩衝](https://aws.amazon.com/tw/blogs/architecture/exponential-backoff-and-jitter/)（jitter buffer）賦予時間一些亂數，避免塞車

對應用程式來說，能做的有限，因此通常都會使用逾時機制，但是需要使用逾時的原因是什麼？

因為我們不知道網路他最長會多久回應。例如，如果我知道網路最久最久一定會在十秒內回我：他找不到目標節點，這樣我就不需要逾時機制了。

這樣另一個問題就來了：為什麼網路延遲是無界的（unbounded）？

### 為什麼網路延遲是無界的

網路封包是需要排隊的，雙向都需要，排隊原因可能為：

-   若訊息量較大，可能會傳送多個封包，不同封包會有不同排隊程度和不同路徑，因此會出現延遲和亂序。
-   如果發現針對特定目標的傳送受到限制，此時很可能面臨*反壓*（backpressure）
-   執行緒排隊，進而影響封包的傳送，VM 因為 QoS（Quality of Service，賦予各執行緒權限等級和重要程度）的關係可能更嚴重
-   壞鄰居（noisy neighbor）

![排隊會讓節點能處理的量大幅下降](https://i.imgur.com/vVgd84c.jpg)

> [Packet Switching Networks Algorithms](https://www.coursera.org/learn/packet-switching-networks-algorithms)
>
> [Stop Rate Limiting](https://www.youtube.com/watch?v=m64SWl9bfvk)

但是有沒有機制是不需要排隊的？想想手機，它在很久以前就出現了，而且通話是非常穩定的，他用了什麼方式？

這裡不會談太多，但是這個資訊的關鍵字是：電路交換（circuit switching） v.s. 封包交換（packet switching）

而之所以網路最終選擇封包交換，是因為成本和效益的權衡考量。

??? note "若有興趣可以展開來看"

    手機通話會需要建立連線，並在這次連線中佔用固定頻寬，由於其他手機不會再來搶這頻寬，所以可以確保他的穩定。

    手機採用的就是線路交換，即使沒有訊號要傳遞也會佔用頻寬，當需要大量資訊傳送的時候又受限於佔用的固定頻寬，硬體使用率整體較低。

    相對而言，採用封包交換的路由器在工作時只需把得到的封包往後送，不用維持連線。除了可以避免路由器被特定連線卡位之外，也能讓路由器專注於轉送封包而非維持連線。

    上面比較的是行動通訊和節點的通訊，若只考慮節點的通訊則會把封包交換和線路交換分別稱為 Datagram subnet 和 Virtual-circut subnet，其比較為：

    | 封包交換和線路交換的比較~issue | Datagram                                                | virtual-circuit                                                  |
    | ------------------------------ | ------------------------------------------------------- | ---------------------------------------------------------------- |
    | circuit setup                  | Not needed                                              | required                                                         |
    | State information              | Routers do not hold state information about connections | Each VC requires router table space per connection               |
    | Routing                        | Each packet is routed independently                     | Route choosen when VC is set up; all packets follow it           |
    | Effect of router failures      | None, except for packets lost during the crash          | All VCs that passed through the failed router are terminated     |
    | Quality of services            | Difficult                                               | Easy if enough resources can be allocated in advance for each VC |
    | Congestion control             | Difficult                                               | Easy if enough resources can be allocated in advance for each VC |
    | Implement                      | Internet Protocal, IP                                   | Asynchronous Transfer Mode, ATM                                  |

    其實還有很多議題來優化你的網路速度甚至限縮網路延遲最大值，包括最佳路徑搜尋、排隊的策略、緩衝的管理等等。

## 時鐘

時鐘的準確性對分散式系統重要嗎？

在討論這之前，我們先來談談什麼是「時鐘」？

### 兩種時鐘

-   當日時鐘（Time-of-Day）
-   邏輯時鐘（Monotoni clock）

當我們在談論時鐘的時候，可能的時鐘有兩種。

當日時鐘會回應當下的時間，例如下午三點四十分十五秒。相對而言，邏輯時鐘的值並沒有真正意義，其價值在於兩個值間的差代表的是精準的時間差，例如第一個值和第二個值差五百奈秒（根據設定差值可能為 500 或者 0.5）。

> 邏輯時間準確性會受多核心影響，每個 CPU 可能有不同的值，但是作業系統會盡量讓你的執行緒每次存取都使用[同一個 CPU 的值](http://steveloughran.blogspot.co.uk/2015/09/time-on-multi-core-multi-socket-servers.html)。

#### 相關程式碼

不同程式碼也會針對這兩種時間提出不同 API。

-   PHP
    -   [time](https://www.php.net/manual/en/function.time)
    -   [hrtime](https://www.php.net/manual/en/function.hrtime.php)
-   Node.js
    -   Date.now
    -   [process.hrtime](https://nodejs.org/api/process.html#processhrtimetime)

### NTP

在講到當日時鐘的準確性時，就必須談到他如何校時的。Network Time Protocol（NTP）便是用來校時的古老協定。

我們會先談所謂的「時間」是怎麼來的，再來談談怎麼校時。

#### 當日時鐘是怎麼來的

![石英震盪器運作原理](https://i.imgur.com/JUMrHc9.png)

石英震盪器（Crystal Oscillator, CSO, XO）是用來計算現在時間的電子元件，他是有誤差的。根據 [Google 調查](https://research.google/pubs/pub39966/)內部資料中心，平均每台機器會有 200 ppm 的誤差，也就是每天 17 秒的誤差。

作業系統透過和 CPU 的溝通獲得其資訊：

```asm
# 設定 ah 的值為 44, 0x2c
mov ah 2ch
# interupt 至 OS（33, 0x21），OS 得知 ah 的值為 44 代表要取得時間訊息
int 21h
```

#### NTP 運作原理

![NTP 運作原理](https://i.imgur.com/vx3MZ2B.png)

NTP 是透過計算來回的時間差來得知節點和中原標準時間的差異，要注意的是 NTP 在校時的時候是一次動一點然後逐漸靠近到正確時間。

但是會有些問題：

-   若相差過大，則會暫停同步並強制重設
-   去回的網路延遲差異過大會大幅降低校時的精準度
-   [閏秒](https://evan361425.github.io/essay/web/ntp/#_1)問題
-   VM 的石英震盪器是虛擬的，也就是會受到 CPU 影響，而降低準確性
-   NTP Server 的[錯誤設定](https://blog.rapid7.com/2014/03/14/synchronizing-clocks-in-a-cassandra-cluster-pt-1-the-problem/)
-   防火牆擋住和 NTP 的連線

#### NTP 之外

除了 NTP 之外，還有哪些校時方式：

-   [歐洲財經市場儀器指南](https://www.esma.europa.eu/policy-rules/mifid-ii-and-mifir)透過高精準的在地時鐘，獲得精準的時間來避免股市的異常。
-   GPS 透過 [Precision Time Protocal](https://web.archive.org/web/20170704030310/https://www.lmax.com/blog/staff-blogs/2015/11/27/solving-mifid-ii-clock-synchronisation-minimum-spend-part-1/)(PTP) 來獲得高精準的時間

這些的成本都很高，且需要專業人員來維運。

### 精準時間重要嗎？

![時間若不準，會讓順序性亂掉](https://github.com/Vonng/ddia/raw/master/img/fig8-3.png)

note:
我們知道了節點時間是不準的，但是回到一開始，精準的時間是重要的嗎？

除了圖上看到的問題，前面我們在講[處理競賽狀況](https://evan361425.github.io/feedback/designing-data-intensive-applications/resolve-race-condition)的時候有提到[_快照隔離_](https://evan361425.github.io/feedback/designing-data-intensive-applications/resolve-race-condition/#_13)，他是利用自動增加的版本來達成一致性，但如果是分散式資料庫，不同的節點就需要一個大家都有「共識」的版本系統。

這時精準的時間就可以被使用了。

### 時間信任區間

![Google Spanner 提供時間的信任區間](https://miro.medium.com/max/1218/1*shHdZkFj2PHtLgpPYCo9Ig.png)

要怎麼獲得精準的時間？如果是透過網際網路傳遞時間，要獲得最精準的時間確實有先天上的難度，但是我們可以在控制的網路狀況中，給予一定信任程度的時間區間，例如：

```
$ curl https://what-time-is-it
{
  "confidence": 95.123,
  "start": "10:00:00.000",
  "end": "10:00:00.100"
}
```

這樣的方式異於在程式語言中要獲得時間（例如 `Date.now`）都是直接給予時間定值而不會透過信任區間的方式。

#### Google Spanner

![Google Spanne 透過在資料中心的高精準時間來讓資料庫叢集有一個一致性的時間戳記](https://miro.medium.com/max/1400/1*kRnwxE6oUJvZCIi9ZA3Gfg.png)

Google Spanner 就是一種資料叢集嘗試透過解決時鐘問題來得到高一致性且高可用性。

!!! info 資料庫文案

    可無限擴充並具備一致性的雲端原生服務，可用性高達 99.999%。（$\dfrac{60*24*365}{100,000}=5.256$，也就是保證每年僅有五分鐘的無法服務時間）

下面是一些 Google Spanner 的白皮書，都不難但是滿有趣的：

-   [intro](https://research.google/pubs/pub39966/)
-   [TrueTime](https://research.google/pubs/pub45855/)

缺點當然是只能在 Google 雲端實踐（需要好的設備加上維運人員）。

### 監控系統

好的監控系統讓你在有狀況時即時知道現在節點的時間狀況，但是這東西比較少去關注。

-   [cAdvisor](https://github.com/google/cadvisor/issues/3068)

## 執行緒延宕

被延宕了代表請求可能會逾時，但是這又如何？應用程式如果考慮 Timeout 的機制等等，這不就解決了？

### 會造成什麼問題？

```javascript
server.on("request", async (req) => {
    // 領袖才會有鎖
    const lock = await getLeaderLock();

    if (lock.isMine()) {
        // 有時限以利重選領袖
        await lock.renewIfNeeded();
    } else if (req.willModifiy()) {
        // 收到寫入請求時轉送給領袖
        return transferToLeader(req);
    }

    return handler(req);
});
```

上述的程式碼是用在*單一領袖*的資料叢集，當*追隨者*收到寫入請求時會轉送給領袖。而判定是否為領袖則是透過鎖，如果該資料庫可以拿到鎖則代表他為領袖，並且為了讓領袖失能時可以轉移權力，這個鎖是有時限的。

狀況來了：如果在執行 `handler` 時，執行緒被延宕超過時限了，會發生什麼事？

這個領袖仍然認為自己是領袖，同時資料叢集又有另一個領袖，這就會造成前面提的*復權*（split brain）問題。

簡而言之，執行緒異常的延宕可能會讓所有的檢查機制都失效。

### 可能有哪些原因

-   OS 層面
    -   VM 會被[暫停](http://www.cl.cam.ac.uk/research/srg/netos/papers/2005-nsdi-migration.pdf)（suspended），被暫停時 Host 會開始把 VM 的資料輸出到 FileSystem 中，並等待問題處理完後復原（resumed），這過程會依賴於系統檔案的 I/O，可能會耗時非常久。
    -   [Memory swapping](https://web.mit.edu/rhel-doc/4/RH-DOCS/rhel-isa-zh_tw-4/s1-memory-virt-details.html) 會讓記憶體不常用的東西放進磁碟中，但是在一些狀況這可能會被反覆觸發。
    -   CPU 會執行[上下文交換](https://tfing.blogspot.com/2019/10/context-switch.html)（context-switch）好讓 CPU 可以有效的被多執行序利用。這就可能造成主要服務被其他服務中斷
-   程序層面
    -   有些動態型別的語言會定期定量執行[垃圾回收](https://www.amazon.com/Garbage-Collection-Algorithms-Automatic-Management/dp/0471941484)（Garbage Collection, GC），[設定不恰當](https://dzone.com/articles/how-tame-java-gc-pauses)可能會讓他延宕程序其他運作（例如商務邏輯的程式碼）的執行
    -   有些語言會定期讀取程式碼，也就是執行資料的 I/O，而這個行為可能會[因為系統磁碟 I/O 效能受限](https://engineering.linkedin.com/blog/2016/02/eliminating-large-jvm-gc-pauses-caused-by-background-io-traffic)而被迫延宕所有相關程序。

### 多一層圍欄

![讓原有的鎖加一層圍欄，避免錯誤認知](https://github.com/Vonng/ddia/raw/master/img/fig8-5.png)

前面提到的可能會有的問題，我們可以透過 [Fencing token](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) 這個機制來避免，不過這裡要注意的是 Client 和 Storage 都會需要存取這個管理鎖的服務，會增加整體架構的複雜度。

## 總結

分散式系統的不穩定讓我們面臨一致性和可用性的選擇，而其解決辦法有：

-   依賴於專門解決分散式系統的工具
    -   [Confluent](https://href.li/?https://www.confluent.io/confluent-cloud/)
    -   [etcd](http://etcd.io)
    -   [ZooKepper](http://etcd.io)
-   穩定的時間
-   如果公司本來就有一系列用來處理錯誤狀態的機制（例如航空公司訂票錯誤、線上商場寄錯包裹），當發生這些少見的競賽狀況時，我們就可以透過既有處理錯誤的機制來回應這些客戶，畢竟如果要讓系統擁有高一致性需要付出一定的代價，而這代價並不會低於日常處理客戶狀態的成本。

--8<-- "abbreviations/ddia.md"
