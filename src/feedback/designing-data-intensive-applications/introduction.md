# Designing Data-Intensive Applications

![Designing Data-Intensive Applications' profile](https://images-na.ssl-images-amazon.com/images/I/51ZSpMl1-LL._SX379_BO1,204,203,200_.jpg)

2020 5 月已銷售 100,000 本，且是 2019 年 O’Reilly 所有作品銷量第二名的作品（第一名是機器學習的）。

!!! info "Martin Kleppmann"

    ![!Martin Kleppmann](https://martin.kleppmann.com/images/martin-kleppmann.jpg){ align=left width=140 }

    -   在劍橋大學擔任資深研究員，並於研究所教授分散式系統。經營一個超讚的[部落格](https://martin.kleppmann.com)。
    -   多項開源軟體，包括 [Automerge](https://github.com/automerge/automerge)，[Apache Avro](https://avro.apache.org/) 和 [Apache Samza](https://samza.apache.org/) 等。
    -   創立兩家公司分別於 2009 被 Red Gate Software 和 2012 被 LinkedIn 收購

**Table of contents**

1.  Foundation of Data Systems
    1.  Reliable, Scalable, and Maintainable Applications【34】[^1]
    2.  Data Models and Query Languages【49】
    3.  Storage and Retrieval【64】
    4.  Encoding and Evolution【54】
2.  Distributed Data
    1.  Replication【61】
    2.  Partitioning【33】
    3.  Transactions【54】
    4.  The Trouble with Distributing Systems【95】
    5.  Consistency and Consensus【110】
3.  Derived Data
    1.  Batch Processing【81】
    2.  Stream Processing【100】
    3.  The Future of Data Systems【114】

!!! quote "身為一個應用程式開發者，我該如何看待本書"

    如果你能夠了解資料庫的內部運作方式，你就能有一個較宏觀和清楚的視野去看待哪種工具或是參數的調校是最適合你的應用程式。雖然本書不會有任何產品的細節介紹，卻會讓你在看資料庫文件時，暸解不同名詞其背後可能代表的優劣勢。

    As an application developer you’re armed with this knowledge about the internals of storage engines, you are in a much better position to know which tool is best suited for your particular application. If you need to adjust a database’s tuning parameters, this understanding allows you to imagine what effect a higher or a lower value may have.
    Although this chapter couldn’t make you an expert in tuning any one particular storage engine, it has hopefully equipped you with enough vocabulary and ideas that you can make sense of the documentation for the database of your choice.

!!! info "資料的重要性"

    [2021 AWS Summit](https://aws.amazon.com/tw/events/taiwan/2021summit/) 提到：統一資料以發揮其價值，成為資料驅動型企業，其特色：

    1. 知識及力量、運用資料擴展企業洞察力和決策權
    2. 將資料大眾化，建立安全系統來收集、儲存及處理資料，提供給需要的人員和應用程式
    3. 以創新方式讓資料發揮功用：資料科學、機器學習

## 報告進程

### 資料模型和語法

對應書中的 _Data Models and Query Languages_，展示各種資料模型[^2]和比較。

!!! question "人際關係"

    假設有 $N$ 個點，點和點的連結就會有 $\frac{N^2-N}{2}$ 個。試想有百萬個社交媒體的用戶，若要使用 MySQL 建立一個彼此之間認識與否的人際網絡會需要多少 entry？這時候有沒有除了 Relational Model 之外的選擇？

    ![](images/graph-model-c1.png){ width=100 }
    ![](images/graph-model-c2.png){ width=100 }

-   Relational Model v.s. Document Model
-   Graph like model and more
-   Query Language

### 索引

對應書中 _Storage and Retrieval_ 的前半段，如何加速資料的讀取。

!!! question "雙索引"

    MySQL 每次下 query 只會遵從其中一個 index，為什麼？若要做多個索引，需要犧牲什麼？

    有些情況必須要雙索引，例如：地理位置中的經緯度，只搜尋經度的話效能的提升有限。

-   Hash index
-   SSTables and LSM-Trees
-   B-Trees
-   and more

### 資料倉儲

對應書中 _Storage and Retrieval_ 的後半段，如何區分線上和後台的資源。

!!! question "數據分析"

    如果我們要分析線上使用者的資料，如何避面和線上使用者搶效能？

-   OLTP or OLAP
-   Column-Oriented storage
-   Stars and Snowflakes schema
-   compression

### 編碼和進程

對應書中的 _Encoding and Evolution_，應用程式和資料庫之間的溝通最佳化和前後相容。

!!! question "舊版編碼如何讀新版資料"

    追求資料體積的極致壓縮，管理也很重要。若資料庫同時存在新版和舊版的資料，如何避免編碼失效。

-   JSON, XML, Binary
-   REST and RPC
-   Message-Passing
    -   Message Brokers
    -   Actor Model

### 競賽情況

對應書中的 _Transaction_，如何避免競賽情況（race condition）帶來的錯誤狀態。

!!! question "訂票問題"

    兩個用戶同一時間訂購限量票種且目前僅剩一張，應用程式利用做 Read-Decision-Write 的機制，會讓兩人同時訂購成功。該怎麼避免？

-   isolation level
    1.  read committed
    2.  snapshot isolation（repeatable read）
    3.  serializable
-   race conditions
    -   dirty read, dirty write（read committed 能處理）
    -   read skew（snapshot isolation 能處理）
    -   lost updates（conflict resolution 和其他方式能處理）
    -   write skew, phantom reads（serializable 能處理）
-   serializable
    -   actual serial execution
    -   two-phase locking(2PL)
    -   serializable snapshot isolation(SSL)

### 分散式資料庫—複製

對應書中的 _Replication_，如何動態複製資料到多台資料庫中，以達成：

-   降低負載
-   高可用性（High Availability）
-   拉近和 Server 請求的距離（Geographically Close）

!!! question "Replica Lag"

    當機器在做複製的時候，若是 **機器A** 完成複製而 **機器B** 還沒，使用者重新載入頁面可能會有不同的結果。

    甚至在複製到 **機器B** 的時候網路中斷，該怎麼達成一致性？

-   algorithms
    -   single-leader
    -   multi-leader
    -   leaderless(Dynamo)
-   trade-offs
    -   synchronous v.s. asynchronous
    -   handle failed replicas（詳細介紹於[容錯的分散式服務](#容錯的分散式服務)）
-   consistency
    -   read-your-writes
    -   monotonic reads
    -   consistent prefix reads

### 分散式資料庫—分區

對應書中的 _Partition_，如何動態分區資料到多台資料庫中，以避免單台機器無法負荷過大的資料量。

![Replication 和 Partition 通常是並行的](images/replica-partition.png)

!!! question "跨機器處理 query"

    當資料被分別放置在兩台機器中，在做 query 時，勢必會增加回應時間。如何避免？

-   approaches
    -   key range
    -   hash of key
-   Secondary indexes
    -   local indexes(document-partitioned)
    -   global indexes(term-partitioned)
-   Re-balance
    -   size of each partition is proportional
    -   number of partitions is proportional
    -   the number of partitions proportional to the number of nodes
-   execute query

### 分散式系統遇到的狀況

對應書中的 _The Trouble with Distributed Systems_，在分散式資料庫下，你會面臨的狀況[^3]和應如何看待。

!!! tip "Debug"

    在找尋錯誤的時候，我們會先假設基礎服務是正確回應的。並在此假設之上開始找錯，當這個錯誤用了兩天（很難重現）去找，你可能就需要開始質疑最一開始的假設了。這就是本章嘗試讓大家去感受的，同時也試著說明[共識](#容錯的分散式服務)的重要性和價值。

-   Unreliable Networks
    -   existence in practice
    -   detect faults
    -   timeouts and unbounded delays
    -   synchronous(telephone network) v.s. asynchronous(IDC)
    -   detailed in [Computer Communication](https://github.com/evan361425/evan361425.github.io/issues/7)
-   Unreliable Clocks
    -   Monotonic(Logical) v.s. Time-of-Day clocks
    -   Synchronization and Accuracy
    -   [閏秒](../../essay/web/ntp.md#閏秒)
-   Process Pauses
-   Build things on unreliable assumption

### 容錯的分散式服務

對應書中的 _Consistency and Consensus_，利用共識演算法達成一致性[^4]和容錯的服務。

!!! tip "觀念"

    共識演算法已經發展幾十年了，仍然有許多待研究的地方，但是它的價值是什麼？

    以機器學習來說，讓其發展蓬勃的價值在於用機器做預測、分析和選擇，那共識演算法呢？

    本書的重點一直都不是對演算法和工具做細節討論，不管是使用 Raft、Paxos 等等的共識演算法，他都是嘗試在[分散式系統遇到的狀況](#分散式系統遇到的狀況)提到的各種問題之上建立一個擁有和多台機器協商並達成容錯能力高的演算法，而又有哪些狀況是可以做權衡的。

-   Linearizability
    -   Lock
    -   Leader election
    -   Constraint and Uniqueness
    -   Cross-channel timing dependencies
-   Ordering Guarantees(Causality)
    -   Total order broadcast
-   Consensus
    -   2 Phase Commit(2PC)
    -   eXtended Architecture(XA)
    -   Fault-Tolerant Consensus
        -   Viewstamped Replication(VSR)
        -   Paxos
        -   Raft
        -   Zab
-   Membership and Coordination Services

---

**前面都在講針對單一應用程式的資料庫，現在試著把把鏡頭拉遠。現在來看看不同應用程式之間的交流、衍伸和整合。**

!!! example "快取"

    最直觀的衍生資料（Derived Data）就是快取，我從資料庫裡拉出一些資料放進快取，加速應用程式進程。

### 批次處理

對應書中的 _Batch Processing_，討論批次處理的優勢和理念。

!!! question "排程工作"

    批次處理（batch job）和排程工作（cron job）是兩件事情。

    排程做 search-index、推薦系統和分析等等，然後再把結果產出在資料庫中。如果程式碼寫錯了，導致線上資料庫崩壞，該怎麼退版到舊資料？

-   Unix Tools and Philosophy
-   MapReduce and Distributed Filesystem
    -   v.s. Distributed Databases(MPP)
-   Beyond MapReduce
    -   What it cost
        -   Materialization of Intermediate State → Dataflow engine
        -   Graphs and Iterative Processing → Pregel processing model
    -   High-level APIs and Languages

### 串流處理

對應書中的 _Stream Processing_，討論事件和處理成串流的機制。

!!! question "抽象程度"

    在丟出事件時，應該要抽象還是實際狀態？

    「求職者A 主動應徵 公司B」v.s.「apply_records insert : userId 11, companyId 24, resumeId 30」

-   Transmitting Event Streams
    -   AMQP/JMS-style message broker
    -   Log-based message broker
-   Keeping Systems in Sync
    -   Change Data Capture(CDC)
    -   Event Sourcing
-   Processing Streams
    -   Usage
        -   Single Use: cache, email, ...
        -   Pipelined: complex event processing(CEP), stream analytics, materialized view...
    -   Handling Clocks and Joins
    -   Fault Tolerance
        -   Microbatch and checkpoint
        -   transactions
        -   idempotent write

### 總結和期許

對應書中的 _The Future of Data Systems_，整合前面的內容，並做出一個強健的應用程式。

![Unbundling Databases](images/unbundle-databases.png)

-   Data Integration
-   One Big Machine
    -   Federated Databases: SQL-like interface
    -   Unbundling Databases: Unix-like
        -   Transaction v.s. Ordered log of events
-   Aiming for Correctness
    -   Transaction v.s. Fault tolerance abstractions
    -   Verifying
-   Doing the Right Thing

## 貫穿本書的目的

一個應用程式需要滿足許多需求才能提供特定服務。

![](https://i.imgur.com/4uYcSaB.png)

-   功能性需求，例如：允許存取資料、搜尋等等。
-   非功能性需求，例如：
    -   安全性（security）
    -   可靠性（reliability）
    -   順從性（compliant with a standard or a spec）
    -   延展性（scalability）
    -   相容性（compatible with a piece of hardware or software）
    -   維護性（maintainability）

### 可靠性

當服務發生狀況時，仍然能正確運行。狀況可能為

-   硬體，通常是無相關性且隨機的
-   軟體，通常是性統性的且難以解決
-   人為

容錯能力（Fault-tolerance）代表他能接受特定狀況的發生，並讓使用者不會受此影響。

### 可延展性

可延展性代表即使流量增加，表現仍是正常的。在討論延展性前，需定義*流量*（load）和*表現能力*（performance quantitatively）。

以 Twitter 的個人首頁為例，利用回應時間的百分位數（percentiles）代表表現能力，每個發布者的寫入和追隨者的讀取首頁作為流量。即使流量增加，回應時間的百分位數仍低於特定水平。

在一個可擴充的系統，我們可以增加機器的量（processing capacity）來維持可靠的表現能力。

### 可維護性

可維護性有很多面向，基本上來說，就是為了讓工程師和運維工程師準時。讓系統保持抽象化（把維度提高）可以降低系統的複雜性，並且讓其更容易修改和適應新的功能。

好的操作性（operability）代表能觀察到系統內部運作狀態和健康檢查，並且擁有高效的方式去管理。

## 結論

通常來說不會有一個辦法可以簡單且完整的讓應用程式可靠、好延展和維護。然而，都會有某種**模式**或**工具**幫助我們一個一個解決這些問題。

<!-- prettier-ignore-start -->
*[索引]: Index
<!-- prettier-ignore-end -->

[^1]: 章節引用數，在我讀書的經驗中，可以把這個當作章節的難易度來做判斷。
[^2]: 本書的中文翻譯都來自[國家教育研究院—雙語詞彙、學術名詞暨辭書資訊網](https://www.naer.edu.tw/)。
[^3]: 在不考慮拜占庭錯誤下。
[^4]: 要注意這裡的一致性和[競賽情況](#競賽情況)中的 isolation 是不一樣的。前者在於分散式系統下的整合多個複製的狀態，後者在於獨立不同的異動（transaction）避免交互影響（維持 isolation）。
