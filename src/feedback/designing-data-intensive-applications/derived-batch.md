# 衍生資料—批次處理

如何利用分散式檔案系統完成批次資料的計算。

![未來資料庫架構的預覽](https://i.imgur.com/pNzIrnw.png)

我們提了單台資料庫[如何在效率和一致性找到平衡點](foundation-ft.md)，這點隨著演進越來越能被大家接受，但是一台資料庫不可能幫我們把所有事情都做好。例如資料大到必須多個節點去處理、需要高可用性等等，我們開始需要使用分散式的資料庫。

然而分散式的資料庫會打破單台資料庫的平衡，我們仍然可以透過共識演算法、2(3)PL 等等維持一致性，但這時效率就會降低。且這些演算法的實作通常都需要非常謹慎的測試和思考，否則任何邊際情況都可能破壞掉預期的一致性保證和高可用性。

有沒有既能擁有高一致性又擁有高可用性然後又能執行複雜的搜尋（例如關聯式資料庫的 SQL）的方案？

有，但是開始前我們需要介紹一些「衍生資料」的工具。

## 簡介

![應用程式需要相依的資料系統是很複雜的](https://github.com/Vonng/ddia/raw/master/img/fig1-1.png)

之前講的資料庫都是假設應用程式使用的單種資料庫，不管是單台還是分散式的。但實際上應用程式是更複雜的，他會有快取、搜尋索引、監控等等不同的資料系統，這次要介紹的就是其中一種資料系統：批次處理。

!!! info "管理和應用的重要性"

    對應用程式來說如何整合不同資料系統和如何使用單一資料系統是一樣重要的！

### 類別介紹

我們先來介紹「資料」是什麼？一般我們會把資料分兩種：

-   原始資料（Source Of Truth, SOT, Systems Of Record)，使用者輸入的資料，例如評論、個資等等
-   衍生資料（Derived Data），利用原始資料產生的資料，例如推薦文章、快取等等

衍生資料的生成通常取決於應用程式的類型，例如社群軟體會推薦可能認識的使用者並快取有興趣的推文，以加速讀取的速度。任何資料系統只是一種工具，根據商務邏輯選擇工具的使用方式是開發者必須要處理的事情。對應用程式而言，使用衍生資料一定會讓程式變得更複雜，該怎麼把衍生資料和原始資料切分清楚（不只是應用面，而是管理面）是一件重要的事。

| 系統類別的比較~類型 | 模式       | 時間 | 注重               |
| ------------------- | ---------- | ---- | ------------------ |
| 服務處理            | 請求、回應 | 短   | 高可用、低延時     |
| 批次處理            | 請求       | 長   | 通量（throughput） |
| 串流處理            | 消化、產出 | 無   | 負載               |

基本上系統可以分三種：

-   服務處理就是我們先前看到的應用程式和資料庫（或和其他服務）的溝通：送出請求（request）得到回應（response）。
-   批次處理概念就是把完整的工作拆分成「批次」（batch），並把每個小份的工作丟給不同節點處理，最後再整合起來。聽起來和我們之前討論的[分散式資料庫的分區](distributed-partition.md)很像，事實上這兩個東西可以說是相輔相成，分區下的並行運算稱為 MPP（Massive Parallel Processing）這兩者已經越來越像，互相學習著，待會會討論到。
-   串流處理則是把請求的概念轉成「事件」（event），每次事件觸發都會引起一系列的異動，而這個異動可能是在多個不同的節點，只要這些節點有在「監聽」（消化）這個事件。

透過這些異於前面我們所提過的資料庫的資料系統，我們就可以建構出一個可靠（高可用、低延時）、高延展和易於管理的大架構。

### 範圍到哪裡

我們會介紹批次處理中的 MapReduce 來幫助我們了解批次處理在做什麼。雖然他已經[過時](https://www.the-paper-trail.org/post/2014-06-25-the-elephant-was-a-trojan-horse-on-the-death-of-map-reduce-at-google/)了，但是他簡單明瞭的運作方式能夠讓我們很輕易暸解批次處理的概念。

當然，在這之上的其他類型的工具和框架也會簡單介紹一下。

!!! info "批次處理的歷史"

    [何樂禮](https://zh.wikipedia.org/wiki/赫爾曼·何樂禮)在 1890 年的人口普查所使用的[打孔卡片製表機](https://www.pcmag.com/encyclopedia/term/hollerith-machine)就是使用機械式的方式聚合人口的資料（[年齡、人種等等](https://www.census.gov/history/www/innovations/technology/the_hollerith_tabulator.html)）。這種利用打孔卡把多個節點的資料整合在一起的方式和現代的 MapReduce 方式十分相似。

    就像我們在[網際網路的進程](https://www.coursera.org/learn/fundamentals-network-communications)上看到的一樣，歷史總是在重複。

## Unix

![GNU Coreutils 是一個基於 Unix 開發哲學建構出的工具組](https://www.maizure.org/projects/decoded-gnu-coreutils/GNU.png)

我們會先透過 GNU Coreutils 了解 Unix 開發哲學，並如何推廣到 MapReduce。

我們透過日誌檔案，嘗試找出一些有用的資訊：

**查看一下資料格式**

```shell
$ head -n 5 11-30.log
2 2021-11-30T08:42:26.728Z 2021-11-30T08:42:27.587Z 858.817257 400
3 2021-11-30T08:42:26.729Z 2021-11-30T08:42:27.590Z 860.616378 400
4 2021-11-30T08:42:26.729Z 2021-11-30T08:42:27.591Z 861.390112 400
1 2021-11-30T08:42:26.726Z 2021-11-30T08:42:27.592Z 865.229151 400
2 2021-11-30T08:42:27.588Z 2021-11-30T08:42:27.596Z 7.301911 400
```

上面的檔案每欄的值分別是 `connection ID`、`start time`、`end time`、`latency`、`HTTP status code`。

**找最低的延時（latency）**

```shell
# 找最低延時
$ cat 11-30.log | awk '{print $4}' | sort -n | head -n 5
```

**查看延時以毫秒為單位的分佈**

```shell
# 透過 less 來檢查輸出的格式，等確認沒問題後再接著執行後續步驟，避免耗時的計算重新執行。
$ cat 11-30.log | awk '{printf "%.0f\n", $4}' | less
# 會發現是長尾分佈
$ cat 11-30.log | awk '{printf "%.0f\n", $4}' | sort | uniq -c | sort -n -k2 | head -n 20
```

> 相關小抄可以參考 [the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh-Hant.md)

### 有哪些哲學在其中

剛剛我們透過 `sort`、`uniq`、`awk`、`sed` 等等的工具完成一系列複雜的運算。GNU Coreutils 的理念便是透過單一介面讓每個獨立的小工具彼此溝通，而這些小工具都能做好自己的事，以下是 GNU Coreutils 在設計時基於的理念：

-   讓各個工具做好自己的事，當有其他功能的需求時，再增加一個工具吧！
-   把輸出設計成其他工具可以拿來用做輸入，避免在輸出中增加無謂的資訊
-   最好在數週內完成設計並實作一個工具，再持續補強
-   盡量使用工具（套件）來減輕開發負擔

什麼是每個工具做好自己的事？舉例來說，`sort` 會把大資料分成小份小份排序好的資料，再把這些資料整合在一起。其中每份資料都是透過不同 CPU 並行處理的，讓整體效率提高到幾乎沒有一個程式語言內建的排序演算法能和他並論的。

!!! info "先人的智慧"

    有沒有很像我們最近的敏捷開發？

### 大致流程是什麼

![GNU Coreutils 的流程](https://i.imgur.com/qtZ27aK.png)

他用什麼單一介面來溝通並達成 **輸入=輸出**？檔案。不同程序透過傳遞彼此的檔案描述符（file descriptor）來告知對方自己的檔案位置，程序再前往該檔案讀取資料。一般來說，檔案描述符有三種

-   STDIN
-   STDOUT
-   STDERR

當他拿到檔案描述符時，上一個程序就會串流輸出進來，並讓下一個程序使用。如果運算必須等到全部算完無法透過串流傳遞的即時資料（例如排序），這時就會一次性寫入。

!!! tip "Linux 內所有東西都是檔案"

    事實上，Linux 系列的作業系統在底層中[不同程序間的溝通都是檔案](https://www.tecmint.com/explanation-of-everything-is-a-file-and-types-of-files-in-linux/)。

    例如耳機透過 `/dev/audio` 下的檔案描述符來作為輸入輸出、本地端的網路溝通則是透過 `/dev/lp0` 下的檔案描述符來記錄相關資訊等等。

所以我們前面看到的 `|` 其實就是上一個程序傳遞自己的檔案描述符給下一個檔案，也就是所謂的管線（pipeline）。讀取檔案時再把 ANSII 編碼方式的 `\n`（`0x0A`）作為定界符（delimiter）。依此，所謂「一筆」資料就出來了。

這是非常厲害的！他讓處理完全不同東西的工具彼此能這麼良好的溝通，想想我們的資料庫即使都是關聯式（或文件式或圖像式），如果要從 _資料庫 A_ 轉移到 _資料庫 B_ 是多麻煩的事。

!!! note "定界符"

    雖然更正確的定界符是 `0x0E`，因為這就是他被設計出來的原因。

    不過最終選擇的 `\n` 也許就是在人類的可讀性和機器的可讀性間的平衡吧。

#### 管線的強大

HTTP 透過 [URL](../../essay/web/url-structure.md) 來指定目的端（不只是 domain，也包括 path、segment 和 query），而這個方式讓網際網路的所有 HTTP 的溝通可以自由切換，這就好像管線功能一樣，所以工具（網站）彼此間的溝通都是通過傳送檔案描述符（URL）。

但是在早期的 BBS 所使用的網路協定主要是 BNU/UUCP 或是 Fidonet 通訊協定，使用者端透過撥接軟體通過數據機撥叫該 BBS 站台的電話號碼來連接進站，這就代表當需要轉到別的站台時，我們需要退出現有站台，輸入目標站台的電話號碼，再輸入細部的位置（以 URL 為例就是 path + segment + query），這就讓不同網站的溝通變得非常困難。

### 比較

和其他程式有什麼差？

```javascript
function getLatencyDistribution(filename) {
    const stream = readFileLineByLine(filename);
    const counter = {};

    for (const line of stream) {
        const latency = line.split(" ")[3];
        const latencyInt = parseInt(latency, 10);
        counter[latencyInt] = (counter[latencyInt] || 0) + 1;
    }

    return Object.entries(counter)
        .map((entry) => ({ latency: entry[0], count: entry[1] }))
        .sort((a, b) => a.latency - b.latency);
}
```

JavaScript 寫出來的函式一樣可以完成工作，但是當我需要調整產出，例如以數量來排序而非以延遲來排序，就要進去程式碼裡面暸解整個結構再做調整。相對而言 GNU Coreutils 就很單純了。

除此之外，我們可以看到 JS 程式碼裡面他的 `counter` 是使用記憶體來記錄這些數量，但是如果當粒度調到很細的微秒等級時就很可能出現記憶體不夠的狀況，相比較而言 `sort` 和 `uniq` 的組合，因為是使用檔案系統做紀錄（和少量的記憶體）就可以避免這件事的發生。

!!! tip "sort 和 uniq 不那麼依賴於記憶體"

    `uniq` 的做法是只找前後文是否有相同的字來做記數，這樣就可以避免全文檢索。所以我們才需要在 `uniq` 之前先 `sort`。

    而 `sort` 會把檔案拆成一小塊一小塊（批次處理的概念！），然後各自排序再整合在一起，就好像我們前面看到的[排序字串表](foundation-index.md#_8)。

GNU Coreutils 的好處不僅僅是方便且有效，他也可以透過自己寫工具提高彈性度。

```python title="透過 Python 寫自己的程序 myProcess"
import os # (1)

r, w = os.pipe()
fr = os.fdopen(r, "r", 1)
fw = os.fdopen(w, "w")

while fr.readable():
  output = myProcess(fr.read())
  fw.write(output)
```

1.  Python 很適合自己設計小工具，當你把上述程式碼寫好之後，你就可以 `pip install -e $LIB_FOLDER` 來產生自己的工具了。

#### 缺點

當然 GNU Coreutils 還是有些缺點的：

-   他在呼叫欄位的時候不是那麼直觀，例如前面的例子中 `{print $4}` 代表的是延時。
-   當資料不再是使用預設的方式做分割的時候，就需要參照很多文件
    -   例如原本是以空格為定界符，當需要使用如 CSV 以逗號為定界符的檔案時就很麻煩
-   有時候輸入有很多，不再只是單純的空格區分的文字時就會很麻煩
    -   例如 `curl` 是用來呼叫 HTTP 請求的工具，HTTP 請求的輸入有很多種：資料（body）、標頭（header）、驗證資訊、是否使用 proxy 等等。

#### 高容錯性

最後再提一下 GNU Coreutils 的重點：高容錯性。

任何輸入的檔案只做讀取，並輸出於其他檔案（或螢幕），你不用擔心輸入在傳入這個工具之後會受到損壞。這也代表你可以反覆嘗試調整工具的使用，或者當有任何問題時重新嘗試不同方式，這是一個非常重要的功能，我們也會在後面再一次看到這種機制的好處。

## Hadoop

我們了解了 Unix 的哲學的好處很多，但是有沒有辦法轉移到分散式的系統呢？

| 分散式的 Unix 就是 Hadoop~分散式 | 單台           |
| -------------------------------- | -------------- |
| Hadoop                           | Unix           |
| HDFS                             | 管線           |
| MapReduce                        | 在這之上的框架 |

Hadoop 就是分散式的一個大 Unix 系統。而這之中 Hadoop Distributed File System(HDFS) 就是 GNU Coreutils 使用的管線。

而我們會介紹的 MapReduce 就是這之上的其中一種框架。

### HDFS

-   HDFS 是 [shared-nothing](distributed-replication.md#_4) 的架構
-   daemon-based，每個節點都會放一個守護程序（daemon），然後這些程序會和一個中央管理人（schedular）去分配資料、備份、提供健康檢查等等
-   備份（replicate），異於我們在[分散式資料庫看到的複製](distributed-replication.md)，他處理的機制和單台機器做檔案系統的備份比較像，例如 [RAID](https://zh.wikipedia.org/zh-tw/RAID)（透過網路）和[糾刪碼](https://www.gigabyte.com/tw/Glossary/erasure-coding)（erasure coding）。

HDFS 是開源軟體，他有很多其他相似的產品，但大致上的邏輯是一樣的：透過無共享架構建構出多台節點交換資料的機制

-   [GlusterFS](http://www.l-penguin.idv.tw/book/Gluster-Storage_GitBook/index.html)
-   [Quantcast File System](https://github.com/quantcast/qfs)
-   [OpenStack Swift](https://docs.openstack.org/swift/latest/)
-   GFS → [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system)
-   Amazon S3
-   Azure Blob Storage

### MapReduce

在介紹 MapReduce 之前我們先看看應用

![以 Lucene/Solr 解釋 MapReduce 的運作](https://i.imgur.com/sQWXHL7.png)

例如 [Lucene/Solr](https://docs.cloudera.com/documentation/enterprise/5-15-x/topics/search.html) 就是透過 MapReduce 在分散式資料系統中產生索引（Index）。

全文索引的建立方式是透過以名詞和文章編號做 key-value pair。舉例來說，`蘋果: 1,6` 代表有 `蘋果` 單詞的文章有 `1,6`。當然實際可能更複雜包括模糊索引、同義詞、錯字搜尋等等不過先以此為基礎來討論。

當使用 MapReduce 時，就會變得很單純：把所有文章分區到不同機器，讓各自去剖析出單詞（map），最後合併（reduce）成上述的鍵值組。你可能可以寫幾個工具去做不同的事，例如有一個工具是把文章拆成單字，一個工具是把單字做統計，不過每個工具都是一組 MapReduce。

這就像是一個黑盒子，文章進來索引出去，透過另一種面貌審視資料。然後當文章有異動時，就重新再跑一次就可以了（為了節省計算資源，這部分是可以被優化的，例如只跑必要的資源），非常單純。

從上例來看對於 Map 和 Reduce 的工作就相對單純了。

-   Map 負責把想要的資料從原始資料提取出來，我們稱其為 Mapper
-   Reduce 負責把相似的資料整合起來並做計算，我們稱其為 Reducer

![Mapper 和 Reducer 做的工作](https://github.com/Vonng/ddia/raw/master/img/fig10-1.png)

當 Mapper 把事情都做完了之後，會通知中央並讓中央通知 Reducer，這時 Reducer 會開始跟 Mapper 要資料。Reducer 這一系列要資料、把得到的資料排序就叫做 `shuffle`（這和我們常見的隨機性不太一樣，需注意避免搞混）。

一組 Mapper 加 Reducer 稱為一個**程序**。而每個程序輸出的結果都會丟進 HDFS 中。

要注意的是，每次 Mapper 的輸出都會做到排序的動作（就像我們前面 Unix 例子中的 `sort`），並把排序後的結果重新分配給不同節點的 Reducer。

#### 工作流程

![工作流程是什麼？](https://i.imgur.com/oEHL45r.png)

就像 Unix 那樣，單一個程序可以做的事情有限，但是透過組合多個程序就可以創造出高效又快速迭代的應用。這一整串的程序稱為工作流程（workflow）

然而 MapReduce 不像 Unix 那樣可以傳遞檔案描述符，他是透過輸出到指定資料夾後讓下一個程序取得該資料夾下的資料作為輸入來傳遞其輸出，這是有好有壞的待會我們再一起。

隨著工作流程越來越複雜，會需要一個好的管理系統幫忙監督這些程序。這時類似 Airflow 的工作流程管理人（workflow schedular）就出現了。

#### 聯合

很多時候我們不會只看一個檔案，我們可能會多個檔案同時使用，就好像關聯式資料庫的聯合（Join）和群組（Group）。但是在 MapReduce 中要怎麼實作？

![使用者的活動和使用者的資訊做聯合](https://github.com/Vonng/ddia/raw/master/img/fig10-3.png)

圖上的範例是找出「拜訪透定路徑（path）的人的年齡」，所以就需要把使用者的活動和使用者的資訊做聯合。這時我們可能得出的結果就會是：「拜訪路徑 /x 的人的出生年份為 1989 的人數是 x 人」：

```text title="拜訪路徑 /x 的人的出生年份為 1989 的人數是 5 人"
/x 1989 5
/x 1990 6
/y 1991 3
...
```

這裡就可以看出聯合和群組在 MapReduce 中其實是非常像的。他們都是從 Mapper 中得到某些排序且整合在一起的資料之後，做一些計算。

!!! info "名詞"

    因為這裡的聯合是在輸出 Mapper 並排序前做的，所以這種聯合方式叫做 sort-merge joins，也因為真正得到聯合的資料是在 Reducer，所以也叫做 reduce-side joins。

##### 如何處理熱點偏斜？

就像我們[在分散式資料庫的分區裡看到的](distributed-partition.md#_6)，如果使用者是名人，這一樣會有熱點的問題，我們有幾種做法：

-   把熱點（名人）的資料送給多個 Reducer 而非只有一個，然後再把需要聯合的資料（名人的資料）送給這些 Reducer，最後再把 Reducer 中相同的資料整合在一起，如 Pig 的 skewed join 和 Crunch 的 sharded join
-   使用 map-side join（待會提）
-   分兩個程序執行，第一個先打亂資料，第二個把打亂的資料整合在一起，例如原本資料叫做 `user1 year30 /url/x` 變成 `123 user1 year30 /url/x` 好讓他可以被打亂。當整合好之後，再透過 `user1` 整合起來。

##### Map-side join

我們也可以在 Mapper 這邊做聯合，這時這種聯合就叫做 map-side join。

-   廣播聯合表，如果待聯合的表是夠小的，就可以直接傳遞聯合表到各個 Mapper 中（這名稱的由來）
-   分區聯合表，如果知道 Mapper 的輸入範圍，就可以把特定範圍的聯合表放進來，減少不必要的記憶體空間，在 Hive 中這稱為 bucketed map joins
-   分區且排序聯合表，如果 Mapper 的輸入不僅知道範圍，也確定他是排序過的（通常這代表這個 mapper 資料源是別的 MapReduce 程序）就可以按照順序讀取特定的值，就不需要把所有的表放進記憶體中間。

##### 比較兩者

Map-side join 的輸出和不做聯合的輸出差不多，相對而言 Reduce-side join 的輸入會受限於你要做聯合的鍵。但是 Map-side join 卻受限於聯合表的樣子， Hive 的 metastore 和 Hadoop 的 HCatalog 就是用來記錄這些聯合表的特性。

我們實際在使用的時候，其實很難去選擇應該要用什麼聯合方式，所以這時候就出先高維度的工具（如 Pig、Hive 等等，這邊我們待會也會在提到），在底層幫我們自動去選擇這些東西。

### v.s. MPP

還記得之前在討論分區的時候有提到 Massive Parallel Processing(MPP) 嗎？他是透過分區讓不同節點的**資料庫**處理各自擁有的資料。我們下面就來看看兩者間的差異吧。

#### 資料結構

![生資料可以根據需求任意變更應用](https://i.imgur.com/rY7J5VE.png)

批次處理的資料是生的（Raw），相對於 MPP 是結構化的（schema）

上面提到的「生」代表他不需要先仔細而謹慎地把資料結構化就可以直接儲存，當未來需要轉成任何商務邏輯的結構都可以，這也是所謂的壽司理論（Sushi）：生的比熟的好吃。這之中的應用有些人會稱為資料湖（Data lake）或企業資料倉儲（enterprise data hub）。

當資料可以輕易轉成任意格式時，跨單位的合作就能輕易達成，例如 _團隊 A_ 想要拿 _團隊 B_ 的資料時，他不需要閱讀繁瑣的文件等等，可以直接拿原始資料做任何轉換加速創新的開發。

也因此 Hadoop 常常被應用於 ETL 之中，當任何線上資料更新時，我可以先把原始資料存進 HDFS，再利用 MapReduce 轉成需要的 _資料倉儲_ 格式並置入其中。

#### 容錯性

![批次處理的流程保證其容錯性](https://i.imgur.com/9RwOM0j.png)

批次處理可以做到 roll back。

批次處理適合機器學習、推薦系統等等，這些應用的產出通常都代表著：我利用原始資料（SOT）產出一組新的衍生資料（Derived data），例如，使用者編號和推薦產品編號的鍵值組。產出的資料就可以放在任一台節點的資料系統中，並透過資料庫讀取該資料提供搜尋。這過程也代表任何一組新的產出如果有任何錯誤，都可以很快速的切換到舊版本，就好像應用程式的 roll back 機制。

可以拿這些檔案提供搜尋的資料庫可能有：

-   [Voldemort](http://static.usenix.org/events/fast12/tech/full_papers/Sumbaly.pdf)
-   [Terrapin](https://web.archive.org/web/20170215032514/https://engineering.pinterest.com/blog/open-sourcing-terrapin-serving-system-batch-generated-data-0)
-   [ElephantDB](http://www.slideshare.net/nathanmarz/elephantdb)
-   [HBase](https://blog.cloudera.com/how-to-use-hbase-bulk-loading-and-why/)

這樣容錯的機制異於以前 MPP，當你更新資料之後通常代表著資料庫的資料確實被異動了。

#### 重來的機制

![MapReduce 在發生錯誤時可以從中間重來](https://i.imgur.com/kXIdEBl.png)

由於每次執行程序後，都會把輸出丟進 HDFS，這樣就可以確保在下一次的程序執行中斷之後，可以利用已經在磁碟中的資料直接重複運行該程序。這方式異於 MPP 會直接捨棄（abort）該請求或者全部重做（還記得原子性嗎？）。

但問題是，有需要做到這麼容錯嗎？電腦不是不常壞掉嗎？

因為批次處理的重要性通常低於處理線上請求的機器，處理線上請求的節點對於高可用性的要求非常高，這時在共用資源的環境下（例如雲端可能都是在同一個實體不同 VM）會把批次處理的程序重要性（priority）調低，當其他重要性高的程序需要資源（CPU/記憶體）時，批次處理就很可能被中斷。

以 [Google 的統計](http://research.google.com/pubs/pub43438.html)來說，每個小時有 5% 的機率會因為其他程序的關係導致程序重跑。

所以在 MapReduce 中，每個程序結束都把結果丟進 HDFS 聽起來就合理多了，因為每一個工作流可能跑一次都好幾小時，若中斷時不能正確重複上一個程序就會很浪費資源。

#### 小節

| MPP 和 MapReduce 的差異~面向 | 批次處理 | MPP    |
| ---------------------------- | -------- | ------ |
| 資料                         | 生/原始  | 結構化 |
| 產出                         | 衍生資料 | 報表   |
| 復原                         | 輕易     | 較難   |
| 彈性                         | 高       | 低     |
| 直觀                         | 低       | 高     |
| 容錯                         | 容易     | 原子性 |

我們整理一下兩者差異：

-   資料結構，批次處理的資料是生的（Raw），相對於 MPP 是結構化的（schema）
-   產出，MPP 通常是產出某種報表（例如，使用者這個月的購買力），批次處理通常產出另一種面貌的資料（例如，使用者的推薦好友）
-   復原性，批次處理因為只是輸出「檔案」，相對於 MPP 的輸出可能會異動資料庫的資料，這種可復原的操作是相對高容錯的
-   彈性，批次處理因為天生允許應用程式客制自己想要的邏輯，所以彈性很高
-   直觀性，MPP 的操作很直觀，尤其透過 SQL 這種抽象語法，讓使用者可以很快速上手（甚至不需要會寫程式的人都可以用）
-   容錯性，對批次處理來說，每一次的異動都不會影響輸入，所以當節點失能時通常都會自動重新嘗試上一個程序（而非全部重試），這點異於 MPP 會捨棄請求（或全部重試）並讓應用程式（或使用者）決定下一動

上面的比較其實相對早期，待會在介紹資料流引擎（dataflow engine）時，我們會再做一次比較，這時候會發現隨著演進，批次程式和 MPP 其實正互相學習著彼此的優點（就好像 CISC/RISC 的關係）。

### v.s. Unix

再來比較一下 MapReduce 和一開始討論的 Unix 吧！

相性性：

-   可輕易重試，輸入並不會被異動且可以無負擔的重新嘗試程序
-   高彈性，任何轉換都可以透過客制的程式碼
-   復用性，任何輸出都可以再被其他人拿來當輸入（介面單一）

!!! danger "不確定性"

    有時計算不是確定性的（deterministic），也就是相同的輸入會產生不同的輸出（可能依賴於外部資源或隨機狀態），這時就很難保證容錯性（無法輕易重試）了。

差異性：

-   Unix 是文字類型的輸入輸出，MapReduce 是使用編碼後的檔案（Avro、Parquet 等等）
    -   因為使用編碼，所以不會有所謂的 `{print $4}`，而是 `{print $latency}`
-   MapReduce 把一個程序拆成 Mapper 和 Reducer 兩段，這會造成問題：
    -   無謂的排序
    -   在進行下一個程序之前會等前一個程序做完，Unix 大部分情況是採用串流機制
    -   Mapper 通常是冗贅的，直接讓 Reducer 使用輸入即可
-   不同程序之間會把資料備份進 HDFS 中

## 資料流引擎

為了解決上述 MapReduce 的缺點，新型態的框架就出現了：Spark, Tez, Flink。

![資料流引擎的流程](https://i.imgur.com/dkl1gNP.png)

異於 MapReduce 讓每一個子程序彼此獨立，最後再整合一起，他們會把全部的程序當成單一個工作（job），這種模式稱其為資料流引擎（dataflow engine）。單一工作中會有多個運算子（operator）就像 MapReduce 的單一程序一樣，只是不同的運算子之間的溝通有幾種模式：

-   傳遞相同的分區資料，這時節點的資料就不需要透過網路傳遞
-   傳遞該分區資料到所有節點
-   重新編排分區資料，MapReduce 預設全部都是如此

!!! tip "回憶一下批次處理的意義"

    記得前面提的：批次處理就是把資料分成一塊一塊丟給不同節點處理。也就是每個運算子（程式碼）會注入進各個節點，並分配相對應的資料分區讓他運算。

### v.s. MapReduce

這些框架和 MapReduce 差異造成的影響有：

-   降低無謂排序（每次 Mapper 結束都要排序）的耗能
-   不需要冗贅的 Mapper
-   運算子間的資料不會丟進 HDFS，避免無謂的耗能
-   透過明確表達運算子之間的溝通，可以有一個概觀了解不同運算子的關係，來達到效能最優化（正確分配分區，就不需要把資料一直傳遞到網際網路中）
-   不需等待前面的運算子完成就可以開始工作（如同 Unix 一般）
-   使用相同的程序運算不同的運算子避免程式碼的初始化耗能

#### 要怎麼重來？

運算子間的資料不會丟進 HDFS 就代表當有節點失能時，需要知道該資料分區是哪些資料，這就需要一個中央管理系統。例如 Spark 使用 Resilint Distributed Dataset(RDD)、Flink 定期設置檢查點（checkpoint）。

透過瞭解運算子之間的關係（還記得前面提的三種關係嗎？）就可以決定上一動的程序輸出從哪邊拿。

#### 其他延伸

因為批次運算在分散式系統的發展趨於成熟，開發者開始關注很多其他議題：

-   圖像式處理：不再是以節點為資料分區的單位，而是以點（vertex）為單位。並且每次迭代只處理相關資料，就好像 MapReduce 中的 Reducer。代表是 [Pregel](https://kowshik.github.io/JPregel/pregel_paper.pdf)。
-   怎麼讓開發者專注於商務邏輯的開發，而不是批次處理底層的運作，並透過抽象介面，讓批次處理的工程師可以提升相關效能而不影響開發者（就好像 SQL 的演進一樣）。相關提高維度的工具，如：Pig, Hive, Cascading，就是可以抽換底層的框架（MapReduce, Spark, Flink）而使用相同的介面來執行批次運算。
-   加速測試，就好像 Unix 中的 `less` 一樣，可以看到部分的運算結果而不是全部跑完

### v.s. MPP

| MPP 和資料流引擎的差異~面向 | 批次處理    | MPP        |
| --------------------------- | ----------- | ---------- |
| 資料                        | ~~生/原始~~ | ~~結構化~~ |
| 產出                        | 衍生資料    | 報表       |
| 復原                        | 輕易        | 較難       |
| 彈性                        | ~~高~~      | ~~低~~     |
| 直觀                        | ~~低~~      | ~~高~~     |
| 容錯                        | 容易        | 原子性     |

資料流引擎和 MPP 正互相學習：

-   MPP 越來越能接受客製化的計算，例如 [MADlib](http://www.vldb.org/pvldb/vol2/vldb09-219.pdf) 允許一些機器學習的演算法進 MPP 中。
-   批次處理也越來越多高抽象的語法減少開發者去設置一些細部參數如[陣列化計算](http://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf)、聯合種類的選擇等等。
-   有些 MPP 的資料結構也允許生的資料結構，例如 [HBase](https://hbase.apache.org/book.html#arch.overview.hbasehdfs)。

## 總結

_批次處理_ 不是排程打 API，而是把資料分成一小塊一小塊，讓多個無共享的節點平行運算。

本次分享的順序大致如下：

-   Unix philosophy
-   MapReduce on Hadoop
-   MapReduce v.s. MPP
-   MapReduce v.s. Unix
-   Dataflow engine v.s. MapReduce
-   Dataflow engine v.s. MPP

從這之中也能看出整個批次處理的發展邏輯和背後推動他受到大家關注的原因。不過上面提到的「資料」都假設他是有限的，例如使用者可能就五百萬筆、使用者活動的資料就 50TB 等等，然而現實生活的資料是持續不斷的，例如使用者活動的資料每分每秒都在增加，這樣我們在算排序的結果就會有差異，該怎麼處理？

這就會需要用到下一章的串流處理。
