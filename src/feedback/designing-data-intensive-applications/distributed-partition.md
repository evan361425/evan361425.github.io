# 分散式資料庫—分區

分散資料和運算，使其幾乎無限制地成長。

[HackMD 報告文本](https://hackmd.io/@Lu-Shueh-Chou/Bk7ze-YAF)

![分散式資料庫長什麼樣子？](https://github.com/Vonng/ddia/raw/master/img/fig6-1.png)

我們前面介紹過分散式資料庫的複製，也提過複製和分區兩者是可以獨立區分的。一般來說任一複製的演算法可以搭配任一分區的演算法。

分區幫助我們把很大的資料庫拆成一個一個小小的資料庫。你可以把這些小資料庫當成獨立的資料庫。當有針對他的資料的搜尋進來了，他就可以照著單一資料庫的運作方式執行。

![複製和分區的差異](https://i.imgur.com/Aa18lL6.png)

複製是把資料庫從一個增加到多個，但是分區是把資料庫從一個拆成多個。

這兩個東西要注意的東西都不太一樣，複製要注意的是要怎麼維持兩個資料庫的資料一致性，並處理多個資料庫不同寫入的衝突。

反之，分區則是注重兩個資料庫的互動。資料要流進哪個資料庫？要怎麼執行分析類型（_OLAP_）的搜尋？

在權衡上，複製需要考慮一致性和效能的比例；分區則需要考慮不同區的平衡和資料的連續性。

!!! example "什麼是不同區的平衡和資料的連續性？"

    舉例來說，購物記錄的資料隨機分佈可以讓他很高平衡性，但是當要取得前十筆紀錄時就可能需要遍歷資料庫；
    反之照順序儲存可以讓資料擁有高連續性。但是因為使用者在搜尋購物記錄時幾乎只會找最近的資料，所以會讓大部分的搜尋落在擁有較新資料的資料庫。
    結論：高平衡可以讓每台資料庫都有事做；高連續可以讓搜尋變單純

複製的**趕工**和分區的**平衡**都是用在當資料庫重啟或新增資料庫時的行為。

分區從 1980 年代就開始發展，直到 2010 年左右 NoSQL 的意識崛起，開始考慮更易擴增的架構，又再一次讓大家關注這主題。

除了 NoSQL，Hadoop 架構的 [_資料倉儲_](foundation-dw.md) 也需要有分區的概念，這裡提到的東西到時候都會在介紹 Hadoop 的時候用到。

分區的概念不管是 OLTP 或者 OLAP 都會需要用到。

> 分區的英文名詞很多：partition, shard, region, tablet, vnode, vBucket

## 三大問題

![不同問題的解決方式和要注意的點](https://i.imgur.com/c9uymOI.png)

-   分區要注意負載_偏斜_，其處理方式有：
    -   範圍分區
    -   雜湊分區
-   路由要有共識資料，其處理方式有：
    -   節點
    -   代理人
    -   使用者
-   平衡要減少 I/O，其處理方式有：
    -   固定區數
    -   固定區長
    -   固定各節點區數

下面依次討論。

### 分區

當資料進來，我要讓他去哪一區？

#### 舉個例子

人力銀行登入需要使用身分證字號，今天我們要讓使用者資料在多個資料庫進行分區，並依據身分證字號決定哪個使用者近哪個分區。

-   第一個字母，因為字母是和地區有關係的，這會造成台北的使用者數量大於花蓮的使用者，造成負載偏斜。
-   前四個數字，因為第一個數字代表男女，就可能因為不同月份求職者的男女比例不同（例如退伍時段的求職者中男生大於女生）而造成負載偏斜。
-   後四碼，看起來可以平均分配了，但今天如果我要找台北地區的求職者有多少呢？

> 高平衡可以讓每台資料庫都有事做；高連續可以讓搜尋變單純

#### 整理一下

-   照順序排
    -   容易製造熱點
    -   需要制定邊界
-   雜湊後照順序排
    -   範圍搜尋效能低

我們把上面的例子整理一下，就會發現兩著模式：一種是照著順序排，一種是隨機亂數照順序排。

照順序排就會容易製造熱點（hot spot），造成一台資料庫很忙很忙，其他的就閒閒沒事做。除此之外，這方式也需要讓應用程式設計人員考慮邊界要如何制定。

以身分證字號為例，若我們按照第一個英文字為分區鍵，我們可能是 A ～ B 一組，C ～ F 一組，G ～ K 一組等等。這麼做的原因是不同城市的人的數量不同，所以平均分配會造成負載偏斜。

最後_雜湊_（hash）的方式大部分資料庫都用此方式做分區。但是他會讓範圍搜尋的效能低落，所以有些資料庫甚至不允許分區鍵的範圍搜尋，例如 [Riak](https://web.archive.org/web/20160807123307/http://www.littleriakbook.com/), [Couchbase](http://docs.couchbase.com/couchbase-manual-2.5/cb-admin/), Voldemort，MongoDB 則是會直接對所有資料庫搜尋。

> 這裡討論的都先假設資料不會增加，不需要考慮平衡問題。

#### 熱點

如果特定的值本來就很常被請求，不管用哪種方式都會造成熱點（同一個值經過雜湊後還是長一樣）。

例如社群軟體上的名人，每次發文依照他的使用者 ID（或發文 ID），流量都會被導進該分區的機器。

你可以透過人工方式寫死進特殊的列表，每次該列表裡的人發文，就加上一些隨機的值在文章 ID 前面（也就是一個文章會有多個 ID），幫助分散流量。

例如：[Twitter 3% 的機器專門替 Justin Bieber 服務](http://mashable.com/2010/09/07/justin-bieber-twitter/)

> 當然，這方法需要做工去管理（bookkeeping）這些 ID。然後每次完整的讀取就會需要分散搜尋到多個資料庫中。
>
> 資料庫自動平衡熱點仍是開放研究！

### 路由

當請求進來，我怎麼知道該資料在哪裡？

![路由請求的三大方式](https://github.com/Vonng/ddia/raw/master/img/fig6-7.png)

三種方式，讓資料庫去路由、透過中間人、請求人自己判斷。這三種方式都不難理解，有點像是微服務下，我要怎麼知道對方服務的 IP 的概念，也就是_服務發現_（service discovery）。

> 有很多公司內部發展自己的_服務發現_系統，並把它[開源出來](http://jasonwilder.com/blog/2014/02/04/service-discovery-in-the-cloud/)。

困難的問題是：要怎麼知道資料在誰身上？尤其當資料庫的資料一直透過_平衡_重新分配，知道即時的資料位置就會變得很複雜了。

#### 第三方幫忙管

![ZooKeeper 幫忙管資料儲存位置](https://github.com/Vonng/ddia/raw/master/img/fig6-8.png)

要怎麼知道資料在誰身上？第一個方式是有一個第三方（圖中的例子是使用 ZooKeeper）去紀錄這些資料。

聽起來好像不難，就是再開一個資料庫去放這些資料，但是後面我們會提：當我們需要 _分散式系統_ 去對某種狀態達成一個 [_共識_](distributed-ft.md)，是非常困難的，很多邊際情況會出現。把該演算法實作出來同時也會需要注意很多小細節（有點像是密碼學上的實作），透過一個開源且被大量使用的軟體（例如 ZooKeeper）來專精於達成這件事是相對安全的。

當相關資料被放在第三方之後，上面提到的三個方法的三個對象：資料庫、中間人、請求人，就可以去監控這個第三方的資料並決定請求該送給哪個分區。

!!! info "哪些資料庫有實作這東西"

    -   Espresso 使用 [Helix](http://www.socc2012.org/helix_onecol.pdf?attredirects=0) (其底層仍依賴於 ZooKeeper)
    -   HBase、SolrCloud、Kafka 使用 [ZooKeeper](https://zookeeper.apache.org)
    -   MongoDB 使用自己的 [CSRS](https://docs.mongodb.com/v3.4/core/sharded-cluster-config-servers/#csrs)

#### 資料庫彼此協商

資料庫透過協定（Gossip protocol）彼此告知對方目前資料庫的狀態，並讓使用該資料的請求送過去給該資料庫。

這方式雖然會增加資料庫要做的事情，但是讓其不再需要第三方協助。

[Cassandra](https://cassandra.apache.org/doc/trunk/cassandra/architecture/dynamo.html#gossip) 和 [Riak](https://docs.riak.com/riak/kv/latest/learn/concepts/clusters/index.html#gossiping) 都是使用這方式。

#### 不要自動化平衡

我們前面提到困難的是當資料庫的資料一直透過自動化的_平衡_重新分配，很難即時共識性的知道資料位置。

既然這樣，每次平衡都透過人工的方來去做，並設定好每台資料庫的資料範圍，這樣事情就簡單了 😀。

[Couchbase](https://docs.couchbase.com/moxi-manual-1.8/) 就是用這方式，當 cluster node 被更新的時候，就紀錄這些分區的 metadata。

### 平衡

重新分配資料的時候到了。

資料會越長越大，需要有新的資料庫分擔工作。除此之外，當資料庫減少（壞掉或設定）了，也可能需要重新分配資料。

> 通常資料庫壞掉是會使用[趕工](https://evan361425.github.io/feedback/designing-data-intensive-applications/replication/#_10)，而不是重新平衡，避免無謂的平衡。

#### 基本需求

-   要盡量平均分散
-   不能中斷請求
-   只移動必要的資料

#### 有哪些方式

![平衡有哪些方式](https://i.imgur.com/zRArKUV.png)

這裡的前提是我們已經決定好要用什麼方式分區（範圍分區或者雜湊分區）

-   固定區數
    -   區的數量代表節點最大數量
    -   人工決定該數。
        -   太多會造成管理困難（資料需要被劃分得很細）
        -   太少可能會分配不平均（有餘數）
    -   Riak、Elasticsearch、Couchbase、Voldemort
-   固定區長
    -   當區長到一定大小時，對半拆；太小時則合併
    -   叢集一開始時可能只有一兩個分區，可以設定最低區數
    -   HBase（使用 HDFS 分配各區）、RethinkDB、MongoDB
-   每節點固定區數
    -   新增節點時，舊節點分他一些資料
    -   符合直覺：資料庫越多，區越多
    -   通常適用於雜湊分區
    -   Cassandra、Ketama

> 這些都是背景執行，當確認分配完之後再把流量導過去。

#### 自動化或手動

平衡是耗時耗工的行為，要謹慎的使用自動化，沒用好甚至會導致連鎖反應：因節點忙碌於 OLTP 和平衡分區導致被判定無法正常運作的節點，最終被迫退出時又因為需要調整分區導致進一步的提升其他節點的工作量。

前面我們在提如何路由的時候就有講到一個方法：不要自動化平衡，就是建立在手動平衡是可被接受的這個前提。

Couchbase、Riak、Voldemort 會自動化平衡，但是不會執行這個平衡，而是交由維運人員來按下「確認」的按鈕。

## 其他

-   如何整合不同分區的資料
-   次索引

### Massive Parallel Processing（MPP）

![MPP 運作概略](https://i.imgur.com/UB3wwXn.png "parallel database system - fig1")

> [Parallel Database Systems](https://15799.courses.cs.cmu.edu/fall2013/static/papers/dewittgray92.pdf)

簡單來說就是讓各資料庫做它能做的事，最後再來整合資料。

這東西會很複雜，我們會統一在批次處理討論，不過這裡也能感受到所謂的批次處理（batch processing）和排程處理（cron-job）的差異。

以下是 MPP 不同實作方式的資料庫分類：

| Category  | Example Systems in this Category                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| Classic   | Aster nCluster, DB2 Parallel Edition, Gamma, Greenplum, Netezza, SQL Server Parallel Data Warehouse, Teradata |
| Columnar  | Amazon RedShift, C-Store, Infobright, MonetDB, ParAccel, Sybase IQ, Vec- torWise, Vertica                     |
| MapReduce | Cascading, Clydesdale, Google MapReduce, Hadoop, HadoopDB, Hadoop++, Hive, JAQL, Pig                          |
| Dataflow  | Dremel, Dryad, Hyracks, Nephele, Pregel, SCOPE, Shark, Spark                                                  |

> /[Massively Parallel Databases and MapReduce Systems](https://www.microsoft.com/en-us/research/wp-content/uploads/2013/11/db-mr-survey-final.pdf)

### 次索引

-   本地索引（local index）
-   全域索引（global index）

次索引很好用，但是違背了分區天生的環境，我們有哪些選擇呢？

> 本地索引有時候也叫 document index；
> 全域索引有時候也叫 term index。

#### 本地索引

![本地索引就是讓各資料庫按照原本單台的方式去做](https://github.com/Vonng/ddia/raw/master/img/fig6-4.png)

這方式很單純，就是我在我能處理的地方做好次索引。

但是當我們要透過次索引搜尋的時候（以圖上為例就是搜尋「紅色的車」），需要全部的資料庫都搜尋一遍。

> 所以，有時候透過次索引的搜尋會叫做 _scatter/gather_。

你可能可以在一開始做分區的時候，對主鍵做一些處理，例如紅色的車前綴加個 `r`，但是這樣可能會造成_熱點_，或者會違背資料庫提供的一些天生限制（constrant），例如自動增加的 ID。

!!! example

    MongoDB Riak、Cassandra、Elasticsearch、SolrCloud、VoltDB 都使用這方式。

#### 全域索引

![全域索引的運作方式](https://github.com/Vonng/ddia/raw/master/img/fig6-5.png)

另外替次級索引增加分區邏輯（以圖上為例就是紅色車的 ID 會進到_分區 1_）

這時我們只需要根據這個資料，去找需要的節點就好，雖然可能需要跨節點去找，但不是全部都找過一遍。

但是這會增加寫入時的效能，因為是在寫入，所以就很可能會發生競賽狀況，需要分散式的交易（也就是 _共識_ ）。

!!! example

    Riak、Oracle data warehous、Amazon DynamoDB 都有額外提供這選項。

這種建立額外的資訊幫助我們查找，其實是一個很有趣的題材，我們會在最後一章的時候，透過我們學到的所有工具，再來討論要怎麼有效解這問題。

## 複製延遲

資料庫間的資料只因為延遲而導致不一致。

不只是複製會延遲、當執行多分區的請求時，也會有延遲。

不過這裡我們只會討論在多資料庫因為延遲導致的資料不一致。而且僅談到「延遲」，不會談到任何資料庫無法回應或網路中斷導致的不一致，因為這需要 _共識演算法_ 來幫我們處理。

> 以下圖為例，就是送給 Follower2 的資料被中斷了，我要怎麼復原 Follower1 的資料？

### 讀你寫的資料

![因為複製延遲導致無法正確讀你寫的資料](https://github.com/Vonng/ddia/raw/master/img/fig5-3.png)

因為複製延遲導致無法正確「讀你寫的資料（read-your-own-write）」。這時我們可以在特定情況下利用應用程式的邏輯避免：

-   當在讀你可以編輯的資料（例如，個人資料）的時候，使用 Leader。
    -   如果你可以編輯的資料很多，會導致 Leader 負擔很重
-   紀錄上次編輯的時間，五分鐘內的讀取使用 Leader
    -   當使用者是在不同裝置讀取時，所謂的「紀錄」就無法在應用程式面中做到。

如果資料庫有做分區，因為不同分區有不同 Leader，可以舒緩這狀況。

### 單調讀取

![兩次讀取的前後狀態不一致](https://github.com/Vonng/ddia/raw/master/img/fig5-4.png)

單調讀取（monotonic-read）可以避免使用者第二次請求看到的資料狀態是第一次請求的舊資料。

我們可以強制使用者這次 session 只能看到同一台 replica 的資料。但是 replica 不能服務時，仍會有這狀況發生。

### 順序一致讀取

![因為讀取順序不一樣導致的錯誤狀態](https://github.com/Vonng/ddia/raw/master/img/fig5-5.png)

順序一致讀取（consistent prefix read）和前面單調讀取很像，只是是特指分區時發生的順序混亂。

我們可以透過上次提的[版本向量](https://evan361425.github.io/feedback/designing-data-intensive-applications/replication/#_27)來避免這件事，但是需要有方法管理這些版本。

!!! info "分散式資料庫只能保持最終一致性？"

    這樣聽起來即使我們在單台資料能保持很強的一致性，在分散式資料庫下，就回到最弱的一致性：最終一致性（eventually consistency）嗎？

    是有方法可以達成更強的一致性，但是你會看到很多資料庫文件都說，當使用資料叢集的時候，我們只提供最終一致性，這是因為達成更強的一致性常常會帶來很多效能和高一致性的犧牲。

    我們也會在最後一章討論除了分散式的交易（共識演算法）之外，我們還有什麼好方法可以不犧牲高可用性呢？

## 總結

分區的概念很多都會重見於_批次處理_中，到時會再把這主題重新抓出來討論。

--8<-- "abbreviations/ddia.md"
