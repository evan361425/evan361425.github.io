在開始講 Index 前，我們可以先看一下一個單純用 `bash` 建立的資料庫，並發現其存在的問題：

```bash
db_set () {
  echo "$1,$2" >> database
}

db_get () {
  grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
```

可以看到這個資料庫在寫入時，擁有超高效能，甚至可以說不會再有比他更有效率（軟體面）的儲存方式了。
這種儲存方式稱為 `log`，附加（append）文字至檔案中。這種方式不會考慮之前有沒有儲存過該資料，而是直接新增至檔案尾處。所以並不會清除歷史紀錄。

> 這個方式並未考慮許多問題，例如：多工處理、清除歷史紀錄、容錯、資料毀損

然而，當他讀取時，卻需要把所有文件都讀過一遍。當資料長兩倍時，可以預期他需要執行的時間也會提升至兩倍以上。為了解決這問題，Index 出現了。

## Index

索引（Index）通常是在主要資料下**額外**建立的 metadata，並當有資料需要「寫入」時，更新這份 metadata。

由此可知，在提升「讀取」效能的同時，便需要犧牲部分「寫入」效能。

> 工具的選擇常常都是在做權衡，若情境需要高效能的讀取，那或許就應該考慮添加 Index。

> 以下的 index 都代表 key-value 中的 key 或者說 RMDBS 中的 _primary key_

大家可能很常使用到 Index，例如： user 表格中年紀小於 30 歲且月收入大於 500 塊的 user。
我們設計了兩個 index 分別是年齡和收入，但

-   為什麼 query 時只針對單一個 index 作搜尋呢？
-   同時使用兩個 index 去做搜尋不是非常直觀嗎？

Index 的意義通常是讓搜尋的次數從 `n`（資料總數，例如一百萬）變成 `ln(n)`（搜尋次數，例如三次），在找到特定的資料（群）之後便無法使用 index，因為 index 表格的建立都是以全部資料為基礎。

> 當然，有些樹狀結構（R-Tree）允許多位元的搜尋，下面會做介紹。

```
           [1,5,10]
    [1,3,5]      [6,8,10]
[1,2,3] [4,5] [6,7,8] [9,10]
```

例如上述，找到 1~3 之後，若需要在做 filter，則需要遍歷資料才能達到目的。

## Hash index

以 in-memory 的方式紀錄 key 位置：

| key | offset |
| --- | ------ |
| 1   | 411    |
| 42  | 393    |

```
1,{"a":"b"}
2,{"c":"d"}
...
42,{"e":"f"}
1,{"g":"h"}
```

每次更新或新增 key-value 時，同時更新該 hash index。

### 問題

-   因為是一直新增資料到檔案尾部，如何避免無限制的檔案大小增長
-   檔案格式
    使用二進位的轉換，降低字串、數字等等多樣的變數格式轉換，例如表情符號。
-   如何刪除指定資料
    需要在該 key 中給予特定值（tombstone），當 compaction 和 merge segment 後，會自動捨棄該鍵值。
-   機器重啟時，重新獲得 hash index 需要全文讀取，非常耗時
    會定時定量快照（snapshot）hash index 進檔案，避免機器重啟時的全文檢索。
-   寫入資料到一半時，機器壞掉
    建立核對和（checksums），若核對和有錯，則不使用該值。
-   如何確保同步控制（Concurrency Control）時造成的錯誤，例如 A 資料寫到一半時，B 資料要開始寫入了，B 要如何等 A 寫完
    僅開放一個寫入的線程（thread）。

#### 檔案壓縮整合

當檔案達到一定大小時：

-   把檔案區分成好幾塊（segment），每個區塊獨自紀錄他們的 hash index。
-   當區塊太大時，開始進行壓縮（compaction），把舊的 key-value 捨棄，並把有效資料寫入新的檔案。
-   兩個小區塊可以進行整合（merge）。

> 此行為是在背景執行，若執行到一半有讀寫的請求，會繼續使用舊的 segment，最後壓縮整合完畢後才使用新的 segment，並把舊的 segment 刪除。

> 搜尋時，若在 segment 1 中的 hash index 找不到該 key，就往下一個 segment 找。

### 缺點

-   Hash index 若過大，或者説 key 過多，勢必會大大影響效能。
-   沒辦法快速查詢範圍的 key，例如想知道以 `animal` 為開頭的鍵值數量。

### 應用

-   [Bitcask](https://github.com/basho/bitcask)

## SSTables

該架構原先稱 Log-Structured Merge-Tree（LSM-Tree），後修正部分行為後於[論文](https://static.googleusercontent.com/media/research.google.com/zh-TW//archive/bigtable-osdi06.pdf)中，重新命名為 Sorted String Tables（SSTables）。

如同上述的 Hash index，會把 index 分成好幾個 segment 檔案。SSTable 在分成不同 segment 的同時，會確保每個 segment 的 key 是獨立（non-overlapping）且排序（sorted）的。這樣能確保以下特性：

1. 在做 merge 的過程，可以非常有效率且省空間：

```
      File1             File2             File3
  ┌────────────┐    ┌────────────┐    ┌───────────┐
  │ Apple      │    │ Apple      │    │ Avocado   │
  │ Apricot    │    │ Banana     │    │ Berry     │
  │ Banana     │    │            │    │           │
  │            │    │            │    │           │
  └────────────┘    └────────────┘    └───────────┘
                        Step1
  ┌────────────┐    ┌────────────┐    ┌───────────┐
  │ Apple      │    │ Apple    * │    │ Avocado   │
  └────────────┘    └────────────┘    └───────────┴
                        Step2
  ┌────────────┐    ┌────────────┐    ┌───────────┐
  │ Apricot  * │    │ Banana     │    │ Avocado   │
  └────────────┘    └────────────┘    └───────────┘
                        Step3
  ┌────────────┐    ┌────────────┐    ┌───────────┐
  │ Banana     │    │ Banana     │    │ Avocado * │
  └────────────┘    └────────────┘    └───────────┘
                        Step4
  ┌────────────┐    ┌────────────┐    ┌───────────┐
  │ Banana     │    │ Banana   * │    │ Berry     │
  └────────────┘    └────────────┘    └───────────┘
```

2. 儲存 index 時，不再需要把每個 key 都存起來，因為是排序過後的，存特定幾個 key 再從中間找就好：

| key | offset |
| --- | ------ |
| 1   | 0      |
| 42  | 393    |

> 當我要找 `key 30` 的資料時，只需要找 0 到 393 即可。

3. 因為儲存的 index 是疏散（sparse）的，所以在 key 和 key 之間的資料可以進行壓縮：

> 以上述的表格為例，`key 1` 到 `key 42` 之間的資料進行壓縮（compress）。

### 策略

由上述的一些特性，可以總結 SSTables 在實作上的錯略如下：

-   每次資料進來，存進 in-memory 的樹狀結構（red-black tree 或 AVL tree），該樹狀結構可以保證新的資料會以排序過的方式存進結構中。
-   當樹狀結構越來越大，超過閥值（通常數個 MB），存進檔案（segment）裡。因為已經排序過，所以儲存的效率機戶等於 I/O 的效率
-   當有讀取的請求時，先讀取 in-memory 再從最新的檔案依序讀取。
-   隨著時間進行，持續進行整合（merging）與壓縮（compaction）。

> 當機器壞掉時，in-memory 的資料就會遺失？
> 每次新的寫入需求，都即時 append 到一個特殊檔案中，且不需排序，此檔案每次 in-memory 被清空時，都會跟著清空。此檔案的功能只用來當機器重啟時，重新放進 in-memory 的樹狀結構。

### 應用

-   Google [LevelDB](https://github.com/google/leveldb)
-   Facebook [RocksDB](https://github.com/facebook/rocksdb) - based on LevelDB
-   Apache [Cassandra](https://github.com/apache/cassandra)(類似) - based on Big Table paper
-   Apache [HBase](https://github.com/apache/cassandra)(類似) - based on Big Table paper
-   [Lucene](https://github.com/apache/lucene)（被 [Elasticsearch](https://github.com/elastic/elasticsearch) 和 [Solr](https://github.com/apache/lucene-solr) 使用） - _term dictionaries_

> 雖然 Lucene 是提供全文檢索的引擎，全文檢索比起 key-value 的檢索要更為複雜，但其邏輯類似：以 search words 作為 key，文章的 ID 作為 value。

### 補充

1. 若搜尋的資料是不存在的（non-exist key），就需要所有檔案都閱歷後才能判斷。

> Bloom filters 特殊結構的檔案，會大略描述資料庫的狀態，並告訴你該鍵值是否存在

2. 該以何種順序和時間點進行整合（merging）與壓縮（compaction）。
    1. _size-tiered_ - 新的和小的 segment 會被整合壓縮進舊的。
        - segment 數量少
        - segment 大小會是 4/16/64... 方式倍增
        - segment 間會有 overlapping 的狀況
    2. _leveled compaction_ - 每一層在升級時會做整層的壓縮
        - segment 數量多，第一層檔案數 10 個，第二層是 100 個
        - segment 大小是固定的
        - 每一層（level）的 segment 間不會有 overlapping 的狀況

> 書中提出兩種方式，有興趣可以到[這裡](https://docs.scylladb.com/architecture/compaction/compaction-strategies/)查看更多策略。

更多詳情可以參考 LevelDB 的[實作文件](https://github.com/google/leveldb/blob/master/doc/impl.md)。

## B-Tree

1970 年就設計出的演算法，並被應用於資料庫中。而這也是近代資料庫在做 Index 時最常使用的演算法。

> 上述提到的方法並不會去更新舊有資料，反之 B-Tree 則會去更新。
> 也就是他不需要做壓縮和整合的動作

把資料區分成多個小塊（_blocks_/_page_）

-   每個區塊的大小通常為 4KB，不過實際上仍要考慮硬體的配置。
-   每個區塊都會有一個地址去代表他（類似程式碼中的 pointer，檔名）。
-   有一個特殊區塊稱為 root，每次搜尋都先經過該區塊。
-   區塊分兩種
    -   路徑區塊 - 用來導引至各個區塊，兩個 key 之間的資料即是存放這兩者之間的資料位置
    -   資料區塊 - 用來儲存 key-value

![B-Tree 尋找 user_id = 251 的資料](https://i.imgur.com/CR05Gtx.png)

> ref 數量代表 _branching factor_，以上圖為例即是 6，通常數量為數百。
> 每塊 4 KB，_branching factor_ 500，共 4 層，可以存 256 TB 的資料量

新增或編輯資訊時，直接去到該 `val` 更新即可。
當超過 _branching factor_ 的大小時，就會對半拆開往下一層放：

![](https://i.imgur.com/LBX8wH2.png)

> 由上述也很清楚可以知道，相比於 Log-Structure 的方式，write 的效率會較低。

### 如何增加穩定度

-   由於 B-Tree 會覆蓋先前儲存的值，這時就需要考慮到硬體是怎麼做覆寫的？

    -   機械式磁碟，等待讀寫頭遇到正確位置，開始覆寫
        ![](https://i.imgur.com/X6isCfT.png)
    -   固態硬碟，以固定單位大小寫入，需配合軟體

> 簡而言之，多一種動作，多一層考慮

-   當更新資料時，可能會把 page 拆分兩個，或影響現有資料。做到一半時，機器壞了怎麼辦？
    -   write-ahead log（WAL 或稱 _redo log_）會紀錄舊資料，作為災難復原用。
-   當需要處理多工（concurrency control），一個工人在讀取時，樹狀結構可能是不穩定的（正在調整 B-Tree）
    -   需要利用 _latches_ 演算法來鎖定區塊不被讀取。
    -   由此也可以看出 SSTable 和 B-Tree 在處理這問題的難易程度，SSTable 在壓縮整合的過程都是背景執行的，而不影響現有資料，最終執行完畢才會做更新。

### 如何優化

1970 年到現在，也做了很多優化：

-   災難復原時 WAF 之外，有些也利用快照的方式，建立副本，讓讀取時不必鎖定該樹。
-   不必使用完整的 key，而是在確保獨立性的同時，取用縮寫即可。
-   讓相近的 page 放在 filesystem 的附近，但是當樹狀結構被更新，就需要更深一層的演算法。
-   增加同層附近 page 的地址，加速搜尋
-   一些變形的 B-Tree 會整合 Log-Structure 的功能去做加速
-   ...

## SSTable vs B-Tree

資料庫效能和應用程式的類型有非常密切的關係，所以列出一些點可以做參考：

-   SSTable 適合寫入，B-Tree 適合讀取。
-   B-Tree 較成熟穩定但是 SSTable 正逐漸提升使用比例。

細節：

-   寫入：每次寫入進資料庫的資料，其一生被重複寫入硬體的次數稱為 _write amplification_
    -   B-Tree 每次寫入進資料庫時時，都會寫入至少兩遍（WAL），且每次更新 page 的些微資料，都需要完整重新寫入（因為是改動舊資料）
    -   SSTable _write amplification_ 通常較低且 append 的方式仍讓他有較高的寫入效能，但受壓縮和整合的演算法或使用者設定影響。
    -   機械式硬碟（磁碟）在有順序性的寫入（append）會有較高的效能
    -   固態硬碟因其是寫進晶片裡，適合緊密的資料寫入，故 append 較有效。（雖然韌體會盡量讓寫入保持緊密）
-   記憶體
    -   B-Tree 通常需要較多記憶體，因為每個 page 都是固定大小，代表可能會有很多閒置空間
    -   SSTable 透過反覆壓縮整合，通常使用較少記憶體。但是若是過大的寫入量，可能會導致壓縮整合的速度來不及配合，進而無限量的增長記憶體，最終崩潰，需要替他準備監控系統。
-   有效性
    -   SSTable 因其可能會需要反覆壓縮整合，儘管是背景執行，仍會吃掉機器的 CPU，導致速度降低
    -   B-Tree 其 latency 通常較穩定
    -   除了 CPU，也要考慮資料的 I/O 能力。SSTable 需要壓縮整合，每次暫存的最新資料塊又需要足夠份量的資源來做寫入，導致和新資料的寫入互相競爭，拖慢速度。
-   原子性
    -   B-Tree 中，每個 key 只會有一個 value，可透過鎖定特定 page 來保持原子性。
    -   SSTable 同一個 key 可能存在多個資料，在處理原子性時會需要較費工的演算法

## Index 排序

很多情況我們會需要增加除了主要 index 外的 index（_secondary indexes_），而這類的 index 不一定需要 unique，例如上述例子中的年齡或月收入。

這種情況有兩種方式可以解決可重複性的 index。

1. 每個 secondary index 用 key-value 儲存，其中的 value 代表多個 _primary index_。例如，年齡 20 的 value 有 `[user-1, user-10]`
2. 用 _primary index_ 去整合 _secondary-key_。例如，手機為 09123 的 key-value 為 `1_09123-*user data*`

除此之外，避免同步的困難，都不會把完整資料放在多個 index 的 tree 中，而是存進

-   _heap file_
-   _clustered index

### heap file

所謂的 _heap file_ 就是存放多個同 _secondary index_ 的資料的檔案。

這方法使用起來很單純，因為當檔案有多個資料。例如上述中的 `[user-1, user-10]`，就直接以下列的方式做儲存

```
# ID,Name,Year,Salary
1,John,20,500
10,Marry,20,550
```

而 _primary index_ 的樹狀結構也是儲存 _heap file_ 的位置資訊。例如 user-10 的 value 可能就是 file1-40（第 40 個 byte 開始算起）。但是當資料更新時，就需要

1. 把所有 index 的資料庫都更新檔案位置。
2. 或在舊的 _heap file_ 中存放新的 _heap file_ 的位置，這樣搜尋時間會越來越長

### clustered index

_clustered index_ 類似於 _primary index_，其意義代表存放資料的 index。當透過 _secondary indexes_ 找到特定資料的 _clustered index_ 時，再利用其找到資料。

以 MySQL 的 InnoDB 來說，每個 _primary index_ 就是 _clustered index_。

但是這種方式會需要：

-   額外的儲存空間（多開一個 Index Tree 去存）。
-   額外的搜尋時間

有些實作，會在 _secondary index_ 的地方存些資料（稱其為 _covering index_），有些實作只把資料存在 _clustered index_。

> _cover_ 代表的意思就是，雖僅儲存部分的複寫資料，他卻可以 _cover_ 一些搜尋結果。
> 但是 covering index 也需要花一些功去維持資料的一致性。

## Multi-column index

上述有提到每次 query 只會參考一個 index。但是多個 index 去做篩選會大大加速搜尋的速度，該怎麼辦？

例如：我要搜尋經緯度在 `51.5151` `122.122122` 的商店。若是使用單一把緯度作 index，則可能搜尋到所有經度在 `-180~180` 範圍內的資訊，搞得有 index 跟沒 index 一樣。

簡單的方式是使用 _concatenated index_，也就是把兩個 index 整合再一起。例如，需要搜尋姓和名一樣的使用者，搜尋姓和名的 _concatenated index_：`王` `小明`，但是當搜尋條件改成`小明` `王`？

比起 _concatenated index_，更常使用的方式是重新設計一個儲存 index 的樹狀結構：[R-Tree](https://www.gushiciku.cn/pl/gbAh/zh-tw)。

其他可能需要多維度的 index 場景有：

-   電商需要搜尋長、寬、高的商品
-   人力銀行需要搜尋薪資、距離新店最近的工作

## Fuzzy Index

有時要搜尋的 Index 是文字，而這串文字又是人類語言，這時在做搜尋時就可能需要考慮：

-   拼錯。
-   文法轉換。如：過去式、現在式。
-   同義詞。
-   該詞彙長搭配的詞。如：減肥、運動。

如同 SSTable 會利用稀疏的鍵（sparse keys）去減少 Index 的儲存量，Lucene 的全文檢索資料庫也會把字詞的部分字元作為稀疏的鍵（類似 [_trie_](https://zh.wikipedia.org/wiki/Trie) 樹狀結構）[^lucene]，加速模糊搜尋（fuzzy search）。

其他類型的 fuzzy index 的演算法可能為文章分類、機器學習等。

## 內存資料庫

把資料存進檔案（filesystem）和把資料都存進內存記憶體（RAM）比，有兩個好處

-   當電源切斷，記憶體的資料就沒了
-   便宜

但是為了解決 filesystem 在讀寫的效率平衡，發展了很多機制：Index、File 大小和數量等等。

近來 RAM 越來越便宜，且若資料庫並不需要儲存大型資料，這時便發展出內存資料庫（in-memory database），其種類大致分兩種：

-   不在乎當電源切斷，是否需要維持資料：[Memcached](https://memcached.org)
-   需要維持資料：[VoltDB](https://github.com/VoltDB/voltdb)、[MemSQL](https://en.wikipedia.org/wiki/SingleStore)、[Oracle TimesTen](https://en.wikipedia.org/wiki/TimesTen)、[Redis](https://github.com/redis/redis)、[Couchbase](https://github.com/couchbase)
    -   透過特殊硬體（不斷電系統）
    -   寫 Log，這方法除維持資料，也擁有提供備份、方便分析等好處。
    -   定時快照。
    -   透過其他機器複製資料（replicate）

內存資料庫不僅僅因為讀取時不接觸 filesystem，其儲存的檔案格式已經經過解析（parse），降低了解析所需消耗的效能。這同時也讓內存資料庫允許更多種類的儲存，例如佇列（queue）或叢集（set）。

除此之外，近來也有需多研究，讓內存資料庫不再受限於內存記憶體的大小，當大小超出其負荷時，資料庫會把最久沒存取的資料放進 filesystem 中，類似 OS 在操作大型資料時的做法，然而卻更為精準，而非一次僅能控制一組記憶體區塊。

[^lucene]: http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.16.652
