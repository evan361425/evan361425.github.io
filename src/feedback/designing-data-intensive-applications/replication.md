# 分散式資料庫—複製

為了讓資料庫備份、高可用性、低延時。

[HackMD 報告](https://hackmd.io/@Lu-Shueh-Chou/rkr4mum0t)

## 為什麼

為什麼要讓資料庫進行複製？主要是三個原因：

-   擴增性。單台機器能執行的運算有限，讓資料庫進行複製代表可以用兩台機器的運算能力取代一台兩倍運算能力的機器，進而降低成本（其成本的成長曲線分別是線性和曲線）。
-   高可用性。當機器壞了，服務仍能運行，除此之外有時為了維運（軟體升版）必須要先停止一台機器的服務，等他完成維運再讓他繼續對外服務。
-   低潛時。分散機器於世界各地，讓不同地方的使用者可以就近使用服務，降低潛時。

### 單台機器

單台機器其實在其成長過程也是有一樣的問題。

-   擴增性：隨著一台機器的原始設備沒辦法滿足運算時，我們可以增加他的 CPU/Memory/Disk。
-   容錯性：當部分 CPU 壞了，一些高階電腦甚至允許不關機的情況下置換設備。
-   低潛時：共享磁碟（shared-disk）的架構，雖然單台機器不能分散各地，但是可以在有限區域內透過一些機制[^1][^2]達到多個機器共享同一個儲存空間。

### 無共享架構

這次談的資料庫間的複製都是建立在無共享架構之上，也就是兩台機器是彼此獨立的：一台機器被燒得精光之後，另一台機器仍能正常運行。

但是他們仍然共享某種協定，例如溝通方式都是透過網際網路或者都是在同一個機房使用同一個電力來源。

會採用無共享架構的原因就是因為幾乎沒有限制的擴增性和其帶來的成本僅僅只是線性成長而已。

## 分散式資料庫

分散式資料庫，就是多台資料庫進行對資料的處理。

要讓多台資料庫合作完成應用程式的指令，就需要共同遵守某一個處理機制。這機制可能是

-   有一個 _協調者_ 在幫忙
-   資料庫裡面有一個領袖決定資料怎麼存
-   資料庫各自為政，再共同決定

!!! info

    因為資料是持續變動的 (OLTP)，所以難。

其中在做分散式資料庫的時候，主要會需要處理兩個東西：

-   複製：資料庫間的資料同步
-   分區：把資料分裝

複製需要做同步，而其中的取捨就好像前面在[討論競賽問題](resolve-race-condition.md)時資料一致性的取捨，要求越高的同步率就會面臨較低的效能。然而待會我們可以看到，透過協調者，在資料滿足特定條件下，可以做到兩全其美？

分區會把資料放在不同的資料庫，例如：_使用者 1-50_ 放在 _資料庫 1_，_使用者 51-100_ 放在 _資料庫 2_。其注重的是如何做到索引、資料量的平衡和彼此間的協作。

這裡要注意的是兩者所使用的演算法是可以獨立區分的。一般來說任一複製的演算法可以搭配任一分區的演算法。

### 概略圖

![分散式資料庫長什麼樣子](https://github.com/Vonng/ddia/raw/master/img/fig6-1.png)

複製和分區通常是同時存在的，所以我們會同時利用複製和分區，達成分散式資料庫。他們兩個方式分別要處理的東西都不太一樣：

-   複製：高可用性、備份
-   分區：一台機器不夠裝

不過我們這次會先介紹複製，之後再介紹分區。所以以下的討論都是假設現有的資料量可以用一台機器來容納。

## 怎麼複製？

| 中文     | 統一            | 其他                                                     |
| -------- | --------------- | -------------------------------------------------------- |
| 單一領袖 | leader/follower | master/slave(standby), active/passive, primary/secondary |
| 多領袖   | multi-leader    | master/master, active/active                             |
| 無領袖   | leaderless      | dynamo-style                                             |

三種方法對應前面提的：領袖、各自為政、協調者。以下都會統一說法為單一領袖、多領袖、無領袖。

### 三種方式的比較

![單一領袖、多領袖、無領袖的比較](https://i.imgur.com/VVxjA7L.png)

這三種方式都有其帶來的缺點和優點，接下來我們就是要來談談各自需要考慮的權衡。

然而，不論任何一種複製方式都要面對趕工和同步延遲。

趕工（_catch up_）就是當資料庫停止運作時（用來維修或意外的壞掉），如何讓資料跟上（不管是從舊的狀態或者從完全空白的狀態）最新的狀態。其作法：

-   有領袖的方式就是透過傳播複製日誌
-   無領袖的方式就是定期整併

至於延遲，我們會統一在下一章的分區討論。

> 雖然無領袖沒有把同異步放進去，但實際上，他也是需要被考慮的，只是大部分資料庫實作都是同時存在，異於有領袖時的複製大部分都是純異步。

## 單一領袖

![單一領袖的運作邏輯](https://github.com/Vonng/ddia/raw/master/img/fig5-1.png)

單一領袖就是一台資料庫（leader）負責寫入資料，剩下的資料庫（follower）負責同步資料並提供使用者讀取資料。

上圖中的 Replication streams 即是在領袖得到資料後，把相關資訊傳遞給追隨者，至於「[相關資訊](#_16)」是什麼，後面會提。

![單一領袖的討論](https://i.imgur.com/0nlQzUG.png)

接下來我們就來看看單一領袖有哪些權衡。

順序會是：

-   如何處理趕工問題
-   趕工造成的複權（split brain）
-   再看看單一領袖和多領袖共通的
    -   *同異步*問題
    -   如何複製日誌
-   最後討論一下為什麼不好擴增和為什麼擁有高一致性

### 趕工

前面提的趕工問題，這邊討論三種狀況。分別是

-   當有新的資料庫要進來一起分擔工作時
-   有一台資料庫暫時壞掉，需要從舊的狀態趕工至最新狀態
    -   若該資料庫是追隨者時
    -   若該資料庫是領袖時

#### 新的追隨者

基本上不管哪種複製方式（單一領袖、多領袖、無領袖）都是這樣的順序。若有領袖則把領袖的資料複製到追隨者身上，反之則挑一個最新的資料庫複製。

由於資料是一直持續的（OLTP），當複製過去後，需要有機制讓他把最新資料補上。

機制大致如下：

-   建立、使用快照。大部分資料庫都內建建立快照功能，有些需要外部套件，例如 MySQL 的 [innobackupex](https://www.percona.com/doc/percona-xtrabackup/2.1/index.html)
-   補上最新資料。補上最新資料前，需要知道快照在整個歷程中的位置（PostgreSQL 的 _log sequence_ 和 MySQL 的 _binlog coordinates_），並從這之後使用我們後面會提的*複製日誌*來補齊。
-   晉升追隨者。準備晉升前的狀態我們稱其為 _catch-up_

#### 追隨者重啟

和前面的很像，就是執行後面兩動：補上最新資料、晉升追隨者。

#### 領袖重啟

當領袖失能時，我們需要執行 _故障切換_（failover）的動作。其順序如下：

-   定期探測其是否存活，若時間內沒回應，就判定其失能。
-   透過選舉，或者直接使用前次選舉所得出來的副領袖。不過通常都是選擇擁有最新資料的追隨者。這一類的選舉，若沒寫好就會出現複權問題，因此通常需要使用共識演算法，之後會提。
-   讓大家都知道誰是新的領袖（包括舊領袖重啟後也要通知他）。

#### 領袖失能造成的問題

-   尚未同步的資料如果完全捨棄，會造成下面的問題。
-   多個領袖稱為複權（split-brain）狀況，這時若沒遇到一些邊際狀況你很可能會同時關閉兩個領袖，導致資料庫提供的服務完全中斷。所以即使有些資料庫叢集提供自動重啟領袖的機制，很多維運人員仍然採用[手動調整](https://kb.synology.com/zh-tw/DSM/help/HighAvailability/split_brain?version=6)的方式。後面提的共識問題就會詳細討論什麼邊際情況會造成錯誤判定。
-   太小的時間區間可能會因為網路延遲導致輕易的重啟領袖，增加機器的負擔。

以下是 [GitHub 遇到領袖重啟後，捨棄尚未同步的資料所造成的狀況](https://github.com/blog/1261-github-availability-this-week)

![領袖失能時所遺失的資料可能導致永久性的狀態錯誤](https://i.imgur.com/z6gUixm.png)

其主要原因是因為主鍵有遞增的模式，但是資料庫重啟後，其遞增後的資料遺失了，導致資料不同步。

### 同異步

同異步是需要做權衡的。

![半同步的單一領袖資料庫叢集](https://github.com/Vonng/ddia/raw/master/img/fig5-2.png)

完全的同步會讓延時變得很不穩，同時單台資料庫若壞掉了，就會導致全部資料無法寫入，這就違背了當初建立多台資料庫以提升可用性的原則。

完全的異步又會讓資料的一致性變得很不穩，這也會破壞我們上一次討論的單台資料庫辛苦建立的一致性，讓前面提到的競賽狀況都可能發生。

有些資料庫的做法是取其平衡使用半同步（semi-synchronous），如圖上所示。不過大部分單一領袖的資料叢集都採用完全的異步，以追求高可用性。

---

### 複製日誌

![複製日誌的類型比較](https://i.imgur.com/lsRgEzw.png)

前面提了很多領袖把資料轉到追隨者時會遇到的問題和權衡。但是都沒提他怎麼把資料轉到追隨者的。基本上有三種：

-   透過輸入的語法（SQL、MapReduce 等等）直接複製到其他資料庫。好處是這種方式通常很簡單實作而且傳遞的資料通常很小。5.1 版前的 MySQL 和特定情況下的 VoltDB 都會使用這方式。其帶來的問題：
    -   非常數的資料的傳遞，例如 `NOW()`、`RAND()`、`AUTO_INCR()` 等等。
    -   若資料是有限制條件的，例如 `WHERE <some condition>`，則會要求所有資料庫狀態都是一致的，否則很容易因為狀態不一致導致執行結果不一樣。
    -   資料庫在更新資料時會有很多其他被影響的資料，例如觸發器（trigger）、貯存程序（stored procedure）、參考鍵（reference key）。導致執行結果可能一樣但是資料庫的整體狀態卻不一致
-   第二種方式是直接使用 WAL。前面在討論[索引](db-index.md)的時候有提到兩種儲存方式：日誌結構和頁導向。日誌結構本來就有在維持日誌並持續在背景執行整合壓縮，頁導向則是利用 WAL 保證資料不會被遺失。我們就可以透過這些日誌的資料進行傳遞。PostgreSQL 和 Oracle 等多個資料庫都使用這方式。不過會有些問題：
    -   通常日誌的資料都很細，甚至細到哪個磁碟的哪個 byte 會塞哪些資料。這導致複製日誌的資料不能在不同版本的資料格式間使用，進而增加維運的困難度。
-   邏輯日誌介於上述兩種方式的中間，不會像語法那樣抽象，但又不會細到像 WAL 那樣。例如語法是 `UPDATE users SET age = age + 10 WHERE age < 10` 則可能傳遞更新的使用者 ID 和其更新後的資料。使用這方式的有 MySQL 的 binlog。除此之外，他也方便透過 ETL 等方式製作其他衍生資料。
-   額外補充一種，有可能在傳遞資料時會希望有個中介器幫助我們加上一些客制的商務邏輯修正，例如加密、特定資料的修正和處理衝突等等。這時可以使用 Oracle 的 [GoldenGate](http://www.oracle.com/us/products/middleware/data-integration/oracle-goldengate-realtime-access-2031152.pdf)。你也可以透過觸發器和貯存程序把資料匯進其他表格（table）中來達成一樣的事情。例如 Oracle 的 [Databus](http://www.socc2012.org/s18-das.pdf) 和 Postgres 的 [Bucardo](http://blog.endpoint.com/2014/06/bucardo-5-multimaster-postgres-released.html)。這些方法雖然可以增加很多彈性，但是因為涉及到應用程式邏輯和資料庫邏輯間的轉換所以通常容易有錯而且會增加資料庫的負擔。

### 適合單一資料中心

因為單一資料中心（data center）資料庫彼此之間不會相距太遠，所以適合這種方式。但是如果有任一台在相距遙遠的地方，則會讓這個資料庫叢集的同步性變得很不穩定。

由於資料都是從領袖寫入，所以前面提的單一資料庫下的交易機制可以運行的很順利。但是仍有資料叢集內的多資料庫一致性問題。

## 多領袖

![多領袖的運作模式](https://github.com/Vonng/ddia/raw/master/img/fig5-6.png)

如果單一領袖失能，會有一段時間不能運行，直覺上就是讓領袖變成多個。但是實際上，很少資料庫採用這方式，因為他會帶來很多衝突和錯誤。

如果你的環境只有一個資料中心，那可能就不需要這麼複雜的機制，相對而言當有多個資料中心時，我們就可以用這方式，但是請小心使用。

有些資料庫預設支援多領袖的叢集，有些需要外部工具支援，例如 MySQL 的 [Tungsten Replicator](https://github.com/holys/tungsten-replicator)、PostgreSQL 的 [BDR](http://bdr-project.org/docs/next/index.html)、Oracle 的 [GoldenGate](http://www.oracle.com/us/products/middleware/data-integration/oracle-goldengate-realtime-access-2031152.pdf)

![多領袖的注意事項](https://i.imgur.com/ALvwAr3.png)

前面已經討論完有領袖時需要注意的*複製日誌*和*同異步*。接下來會著重在多領袖需要注意的處理衝突和梳理因果。

順序會是：

-   了解多領袖帶來哪些好、壞處。
-   多領袖的狀況其實滿常見的？
-   介紹不同拓撲（topology）下的情況。
-   因為同時有多個資料庫在寫入，如何處理衝突？
-   如何梳理因果關係。

### 多領袖的好處

在效能上，不只是寫入的資料庫變多，可以分擔，更重要的是可以放置在多個資料中心，這時就可以根據使用者把請求送到比較近的資料中心。

在容錯上，因為放在多台資料中心，任一個資料中心的基礎設施損害並不會造成全面性的停擺。也可以避免單一領袖因為領袖失能導致服務終止的狀況，因為其他領袖會幫忙分擔請求，並等待失能領袖被替換。

### 多領袖的壞處

他會破壞很多資料庫原有的功能，例如，自動增加的 ID、資料限制（constraints）等等。除此之外，當多台資料庫同時寫入時勢必就需要處理兩個寫入的衝突。就像前面提的，有時候衝突不那麼明顯，例如訂票問題。

### 多領袖其實很常發生

例如手機中的日曆應用程式，你的手機即使沒有網路，仍要可以紀錄行程於日曆中，並且在重新上線之後，和資料庫的資料整合再一起。但是整合的資料可能會因為你同一時間又在其他裝置（例如筆電）更新資料導致有衝突。

這情況就好像多領袖的資料叢集，這時同步的延遲可能就不是好幾秒而是好幾天。[CouchDB](https://docs.couchdb.org/en/stable/replication/conflicts.html#replication-conflicts) 就是專門設計處理這種狀況的資料庫。

第二種狀況就是編輯線上文件，例如 Google Doc/HackMD。直得注意的是，當我們在編輯時，通常該線上文件會標示哪個人正在哪個地方編輯，這麼做其實就能大大降低同時編輯相同地方造成的衝突。

### 拓撲

![多領袖會有很多種拓撲](https://github.com/Vonng/ddia/raw/master/img/fig5-8.png)

當領袖超過兩個的時候，彼此間溝通的路徑就會有很多種，上面提的是常見的三種。

MySQL 預設僅支援環狀拓撲，而環狀拓撲和星狀（或稱樹狀）拓撲會賦予每個節點一個 ID，並在複製過程中，在複製日誌中加上各自的 ID，用來代表他已經跑過這個資料。避免該資料一直被丟進複製的輪迴中。

不過環狀拓撲和星狀拓撲都會有個缺點就是當其中一個拓撲斷線了，很可能會導致複製的連結中斷，然後大家必須等他復原。

最常見的是第三種，all-to-all。不過他容易會需要梳理因果，我們待會再來看這問題。

不過重點是前面提的問題都是可以被處理的，但是身為應用程式開發人員，我們需要在該資料庫文件中查找相關說明，然後明確知道沒有這些處理機制時，我們會遇到哪些問題。並實際做過一些測試確保這些保證是符合我們預期的。

#### 單一領袖也有拓撲

![Replication Chain](https://miro.medium.com/max/4800/1*TL6frkbEMlLOwuo6VTL5TA.png)

除了多領袖之外，單一領袖也是有拓撲的。以圖為例就是 [Replication Chain](https://medium.com/coinmonks/chain-replication-how-to-build-an-effective-kv-storage-part-1-2-b0ce10d5afc3)（RC）。

### 處理衝突

我們一直有提到多領袖需要處理衝突，現在我們就來看看怎麼處理衝突。

-   避免衝突。如果可以，把相同的資料的編輯丟給同一個領袖，例如使用者編輯個人資料，就把該使用者的所有寫入請求丟到同一個領袖（也許是離他最近的 DC）。但如果同一時間地球另一邊有人也在編輯相同使用者的資訊時，還是無可避免的有衝突。
-   給予各寫入請求一個時間戳。只讓最新的資訊寫入（Last Write Win，LWW），雖然這很常見，但卻很容易出現資料的遺失。如果又考慮到機器的時鐘是不准的這個議題時，很可能新資料會被舊資料覆蓋，時鐘問題會留到別篇討論。
    -   Cassandra 只支援[這方式](http://www.datastax.com/dev/blog/why-cassandra-doesnt-need-vector-clocks)
    -   Riak 可以選擇使用[這方式](https://riak.com/clocks-are-bad-or-welcome-to-distributed-systems/)
-   高階領袖可以複寫低階領袖的寫入請求。基本跟 LWW 很像。
-   把所有衝突記錄起來並在
    -   下次請求時，要求應用程式（或使用者）整併衝突
    -   發生衝突時，要求應用程式（或使用者）整併衝突

#### 其他處理衝突的領域

-   特殊的資料型別（[Conflict-free Replicated DataTypes](https://speakerdeck.com/lenary/crdts-an-update-or-just-a-put)，CRDTs），例如 Map、counter 等等，天生容許衝突
-   特殊的資料架構（[Mergeable persistent data structures](http://gazagnaire.org/pub/FGM15.pdf)），類似版本控制系統（如，Git），會把衝突記錄起來並依照設定整併起來
-   文字整合（[Operational transformation](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.53.933&rep=rep1&type=pdf)），實作於 Google Docs 中，把字串當成陣列並允許同時插入新值。

上述方式都算新的方式，並且現有的資料庫通常對於衝突並沒有很好的支援，一樣，細看文件，並做測試。

例如亞馬遜以前在[處理購物車的衝突](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)時，他們考慮了添加產品時的衝突，卻沒有考慮刪除時的衝突，導致明明刪除的產品，刷新頁面後又出現在購物車之中。

### 梳理因果

![因果混亂並不是衝突](https://github.com/Vonng/ddia/raw/master/img/fig5-9.png)

因果混亂並不是衝突，以上圖為例，兩個請求並不是並行處理，而是有相依關係的，這時造成錯誤的便是衝突的混亂。

我們可以有的做法就是替各個請求添加 ID，也就是版本向量。

#### 版本向量

![版本向量允許讓應用程式處理衝突和因果混亂](https://github.com/Vonng/ddia/raw/master/img/fig5-13.png)

為了讓事情變簡單，我們先想像只有一個資料庫，了解原理後，再擴展到多台資料庫時就不難了。

1. Client1 請求寫入 `[milk]`，定其為版本一
2. Client2 請求寫入 `[eggs]`，得到版本一的資料 `[milk]`，並在應用程式中整合兩者成為 `[eggs, milk]`
3. Client1 請求寫入 `[milk, flour]`，得到版本二的資料 `[eggs]`，並在應用程式中整合兩者成為 `[milk, flour, eggs]`
4. Client2 請求寫入 `[eggs, milk, ham]` 得到版本三的資料 `[milk, flour]`，並整合成 `[eggs, milk, ham, flour]`
5. Client1 整合成 `[milk, flour, eggs, bacon, ham]`

透過賦予各個寫入請求一個版本，並在每次送出請求時，夾帶現有的版本，來讓應用程式整併（或設置資料庫讓他自己整併）。這不僅可以處理衝突，當發生因果混亂時，我們也可以透過版本去整合衝突。

現在把資料庫擴增到多版本，這時就會得到版本向量（version vector），而非單一版本。

!!! info

    版本向量和時鐘向量（vector clocks）是兩種不同的東西，時鐘向量是用來讓分散式系統獲得一個統一的遞增順序。之後會再詳細介紹，若有興趣可以看一下[文章](https://haslab.wordpress.com/2011/07/08/version-vectors-are-not-vector-clocks/)。

## 無領袖

![無領袖的運作架構](https://i.imgur.com/y8qZWDH.png)

前面兩種方式都是讓使用者送出請求到特定資料庫，但是無領袖的方式是讓使用者（透過協調者）送請求到全部（或大部分）的資料庫。

其實無領袖的概念並不新，但是這概念在早期的效用並不明顯，尤其當時一台關連式資料庫就可以做到很多事情的時候。隨著 Amazon 開始推出 Dynamo 系統時，有越來越多資料庫也支援這類方式的複製。

支援的資料庫有

-   Raik
-   Cassandra
-   Voldemort

有些資料庫叢集內會提供協調者負責送這些請求到各個資料庫，有些則是讓使用者直接呼叫（透過 SDK 等方式）。

![無領袖的討論](https://i.imgur.com/ITEkFRL.png)

和多領袖一樣，無領袖因為每個資料庫節點都會做寫入的動作，所以很可能會造成兩個資料庫的狀態不一致，例如資料庫 1 先寫 A 再寫 B，資料庫 2 先寫 B 再寫 A。

這時就需要處理兩個資料庫間的衝突，還要梳理相關因果。不過大致邏輯是差不多的。

主要差別在於無領袖他需要在各個資料庫間定期整併，所以這段的順序會是

-   如同前面提到的，同異步的選擇，如果單一資料庫損壞，我需要等他復原才能完成請求嗎？
-   如何做到多台資料庫的資料一致性
-   為什麼無領袖可以做到高可用性

### 需要全部送成功嗎？

![只需要部分請求成功就可以視為成功](https://github.com/Vonng/ddia/raw/master/img/fig5-11.png)

同時寫入多個資料庫後，如果其中幾個資料庫因為任何原因（網路延遲、資料庫重啟）無法送出成功，就會導致運行終止。為了維持高可用性和資料的一致性，我們要怎麼選擇允許失敗的請求數量？

以圖片為例，五個資料庫，我只要成功寫入和讀取各三個資料庫，就能確保拿到最新的資料回傳給使用者。

也就是 $w+r>n$，這裡的 $n$ 代表資料庫總數。

不過有些邊際情況會讓這種保重失效：

-   並行的讀取和寫入
-   並行的衝突寫入
-   成功寫入的資料庫壞掉，導致新的資料庫使用舊資料「趕上」
-   時鐘不準導致的問題

#### 鴿巢原理

![CC BY-SA 3.0](https://upload.wikimedia.org/wikipedia/commons/5/5c/TooManyPigeons.jpg "鴿巢原理")

這理論英文稱為 qourum，有些人會翻譯為法定人數，但是法定人數這名詞是用在法律領域的。事實上，這個理論是基於[鴿巢原理](https://zh.wikipedia.org/zh-tw/鴿巢原理)。也就是當我有十隻鴿子，九個鴿巢，我就能保證有一個鴿巢有兩隻以上的鴿子。

有些資料庫為了高可用性，不會滿足鴿巢原理，例如在五個資料庫中僅成功送給兩個資料庫就完成該次請求。

除此之外，有些資料庫當發現沒辦法滿足預定的數量時，會把請求送到原本 $n$ 之外的資料庫（或者放進協調者本身），這種我們稱為稀薄的鴿巢（sloppy quorum）。當原本無法送出的資料庫恢復原狀之後，再讓這些備援的資料庫把資料送回給這些資料庫，這過程稱為提示移交（hinted handoff）。

當資料叢集越來越大，你要送出的請求很多，這代表越來越容易出現無法正確送出的狀況，這時資料庫會越來越難維持一致性。所以需要有一個方法來處理這件事，我們下面就是在討論這件事。

### 維持資料庫的一致性

![讀取時復原](https://github.com/Vonng/ddia/raw/master/img/fig5-10.png)

當不能寫入的資料庫隔了一段時間恢復原狀了，我們會在下次讀取的時候，把這個資料庫的資料合成到最新的資料。這個動作我們稱為讀取時復原（read repair）。

但是這代表，如果資料沒被讀取，他永遠不會原持最新資料，該怎麼背景處理？

#### 定期整併

![透過 merkle tree 讓他定期整併](https://i.imgur.com/D6Q1VfT.png)

dynamo-style 資料庫會使用[反熵](https://slidetodoc.com/dynamo-bayou-101119-adapted-from-andrew-ors-a/)（anti-entropy process）定期讓兩個資料庫的資料達成一致性。透過 Merkle tree，可以快速找到兩個資料庫間的差異，並傳遞彼此的差異來達成同步。

不過並不是所有資料庫有實作這個行為（例如 Voldemort），除此之外反熵並不保住資料寫入的順序，所以很可能會造成資料的衝突。

### 無領袖的優缺點

因為有鴿巢原理，可以保證資料的一致性，並允許部分的異步來達成高可用性。

除此之外，因為鴿巢原理讓他不需要強制等到所有請求送出成功，所以資料庫可以透過異步的方式把請求送到別的資料中心。

然而寫入的請求很可能會在滿足一致性的過程中導致順序被重置，這就代表資料不能過於複雜（dyanmo-style 的資料同常都是 k-v pair），才能讓即使資料寫入順序被打亂，仍能有效運作。

## 其他

當多個資料庫進行複製時，肯定會出現延遲導致資料的不一致。就好像我們上次提的競賽狀況一樣，有哪些狀況跟哪些處理上？複製延遲我們會在下一次的[分區](partition.md)討論！

除此之外，有些資料庫會提供接口，讓維運人員知道現在資料庫的一致性狀況。通常領袖類型的複製方式很好做，透過領袖和跟隨者都比較來找出差異。但是在無領袖的分散式資料庫中，因為資料的寫入是非順序性的，做法就會滿困難的。這領域仍在[研究中](http://www.bailis.org/papers/pbs-cacm2014.pdf)，而且實作的比例較低。

大部分維運機器的成本都是在電量上，若有一個不需要傳送大量資料且傳送的頻率不高的[演算法](https://www.cs.cmu.edu/~fawnproj/papers/fawn-sosp2009.pdf)，就可以省很多錢！

## 總結

-   分散式資料庫
    -   擴增性
    -   高可用性（高容錯性）
    -   低潛時
-   複製、分區

我們開頭談了分散式資料庫的好處。並區分了兩種處理方式—複製、分區。這次集中討論如何做到多資料庫的複製。

![複製的總結](https://i.imgur.com/VVxjA7L.png)

各個複製方式彼此都有權衡，如果你的資料並不複雜，就可以考慮使用無領袖的方式。如果你只需要在單一資料中心建立資料叢集，就可以考慮單一領袖的複製方式。

[^1]: Network Attached Storage(NAS)
[^2]: Storage Area Network(SAN)

--8<-- "abbreviations/ddia.md"