# 資料模型和語法

開發應用程式時，我們所選擇的資料模型種類，決定我們如何看待問題。

[HackMD 報告](https://hackmd.io/@Lu-Shueh-Chou/Hyzgu7EcF)

---

大致上我們專注於以下四種模型，文末會在提到其他模型。

-   階層式樹狀結構（Hierarchical Tree）
-   關聯式模型（Relational model）
-   文件式模型（Document model）
-   圖像式模型（Graph-like model）

一開始資料儲存僅以 Hierarchical Tree 的形式儲存資料，但是當需要考慮到[多對多（many-to-many）](#_4)的關係時，就開始出現困境。

而後，當關聯式模型不再滿足需求，例如：資料格式不想要多做一層轉換、無法快速做 scaling 等等時，便相繼發展出其他模型。

## 關係

資料和資料之間的關係，會決定你應該用哪種模型。所以我們先來梳理一下資料庫中會有的關係吧！

### 一對多

![一對多](https://www.plantuml.com/plantuml/png/SoWkIImgAStDuSh8J4bLICqjAAbKI4ajJYxAB2Z9pC_Z0igNf2eelTYqvzcqTYM5n6A5H2wkH0LTNJk5vrDdlbZHO8Z2CqBX6NCvfEQb04q70000)

這種狀況其實很適合階層式樹狀結構和文件式模型。

### 多對一（多）

![多對多](https://www.plantuml.com/plantuml/png/SoWkIImgAStDuSh8J4bLICqjAAbKI4ajJYxAB2Z9pC_Z0igNf2eeFLiny_d69OPA2ed52YM6gA96454ZL55ZYAWnJFJ5fZtFfhL3J2WmH1KrWeWQSN6L62hewjg159GOmLd6K1PSrWWe2sCvfEQb0DqF0000)

「多對一」和「多對多」很像，若貼文只看一個，就是「多對一」。

階層式樹狀結構和文件式結構在這種狀況下難以儲存，且難以 query。實際就會需要使用迴圈來撰寫。

## 階層式樹狀結構

Conference on Data System Language(CODASYL)是早期發展的階層式樹狀結構搜尋語言。

每個註冊者當作一個樹，註冊者會有年紀和職業。下列程式碼的目的是找到「年輕的註冊者的職業」。

```codasyl
MOVE 'ACCOUNTANT' TO TITLE IN JOB.
FIND FIRST JOB USING TITLE.
    IF NOT-FOUND GO TO EXIT.
    FIND FIRST EMP WITHIN ASSIGN.
        IF END-OF-SET GO TO 0.
            GET EMP.
            IF EMP.BIRTHYR I 1950 GO TO N.
            FIND OWNER WITHIN WORKS-IN.
            GET DEPT.
            ...
            FIND NEXT EMP WITHIN ASSIGN.
            GO TO M.
        FIND NEXT JOB USING TITLE.
    GO TO L.
EXIT.
```

!!! quote

    RH Katz.: "[Decompiling CODASYL DML into Relational Queries.](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.86.3853&rep=rep1&type=pdf)", 1982

由此可以看出，階層式樹狀結構在做這種負責的關聯性的搜尋，常常愛莫能助。

## 關聯式模型

Edgar Codd 在 1970 的 [A Relational Model of Data for Large Shared Data Banks](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)論文中提到，關聯式模型的定義：

-   相似資料被整合進同一關係（relations/tables）中
-   而各個關係裡是一系列的非順序性組合(tuples/rows)。

因為關係被抽出來了，不再有複雜的路徑需要去探索。反之，因為資料都被存放在同一關係下，篩選（`WHERE`）和調整順序（`SORT BY`）就變得很單純。

除此之外，透過聯合（`JOIN`）可以把不同的關係整合在一起。除了解決多對多的關係之外，也可以避免應用程式去考慮一致性（consistency）。例如：

每個使用者對應一個他現在的職稱，在關聯式中是透過不同關係（table）的 ID 去做連結，所以職稱改變只需要調整職稱的關係裡的文字就可以改變所有和其對應的使用者職稱。

### 查詢最佳化器

![Query Optimizer](https://i.imgur.com/xQbiuHt.png)

我們前面看到階層式的樹狀結構在做搜尋時，是每一個需求都要設計一個邏輯，然而關聯式卻不同。

SQL 是關聯式模型在做搜尋語言時的一種協定。SQL 在推出時有個創新思考：_透過一個泛用的最佳化器_，讓你可以用抽象的方式去查詢，而非每次搜尋都要設計一種。抽象化的方式和命令式比較細的比較待會會在查詢語言中討論。

這裡重點是，透過查詢最佳化器，工程師不再需要根據各個查詢（查文章、查留言），去設定獨立的搜尋機制，像上面的樹狀結構那般。

結論就是比起讓大家在各自的請求中，設計一個搜尋機制，不如花很多心力去建立一個泛用的搜尋工具。而歷史證明這個方向是大家較能接受的。

## 文件式模型

這樣看起來，文件式模型好像又如同樹狀結構資料那般，有一些查詢上的先天缺失，他走回頭路了嗎？

確實他在多對多或多對一個關係中仍然不像關聯式模型那麼方便，即使現在有些技術幫助他讓不同文件做聯合，例如透過文件參考（document reference）。

但是，因為他在處理一對多的關係時非常單純，不會像關聯式一樣有各種 join 和 group，讓他在分散式的資料庫下非常好做，這會在我們後面做複製（replication）和分區（partition）時和考慮競賽狀況時更能體會到。

除此之外，還有[綱目](#schema)也不太一樣。

### 綱目（schema）

我們直接來看看實際在取得「使用者 ID 123 的第三個工作經歷」的資料時不同模型的搜尋方式。

**關聯式模型**

```sql
SELECT experience FROM experience_relation WHERE use_id=123 AND index=3
```

**文件式模型**

```javascript
db.get("users.123.experiences.3");
```

兩種不同的取得方式，就可以感受到文件式和關聯式資料庫的儲存方式差異。

關聯式模型需要關係中所有的組合（row）都要有 _user_id_ 和 _index_。所以當你新增欄位的時候，所有舊的組合都會需要更新他的值來保持格式的一致性。雖然大部分資料庫都會讓這機制做比較軟性的限制，例如預設所有舊的資料為 null 時，不會強制讓資料重洗一遍（MySQL 除外）。

文件式模型則是所有資料格式不必一致，僅在我讀取的時候我預設他應該要有值。

所以總結關聯式模型會在寫入的時候就要求資料保有一定格式，我們稱為 **schema-on-write**。

反之文件式模型，在讀取時，應用程式會預設他有某些資料。要注意，文件式模型並非沒有綱目，而是這個綱目較為隱晦，是應用程式在讀取資料時去定義的，我們稱為 **schema-on-read**。

除此之外，當綱目更新的時候，第一種除了在應用程式做調整外也會需要在資料庫做手腳，第二種僅需在應用程式做手腳。

有什麼差別？

-   對資料庫做手腳會不會吃掉線上使用者的效能
-   應用程式可以退版，所以需要考慮臨時有狀況時，退版是否會影響。（forward compatible）

這段細節會在[編碼和進程](./foundation-encode.md)做更深的討論

### 除此之外

關聯式資料庫和文件式資料庫的比較除了上述提到的，還有

-   資料局部性（data locality）
-   資料的轉換（impedance mismatch）
-   思想的轉換

資料局部性是什麼？如果你的應用程式需要拿完整資料來做運算，例如：你要做點餐的系統，你會需要把設計好的菜單拿來渲染出點餐頁面。相對關聯式資料庫需要各種聯合（join）和取得不同 table 的資料，文件式資料只要拿一次就可以。這就是資料局部性，完整的資料在本地位置就可以取得，不需要再去和其他位置拿。

再來，關聯式資料庫通常都需要應用程式去轉換資料的格式。因為你從資料庫拿到的只會是 k-v 的組合，而一般程式碼使用的都是 class 或是 map/array 等等。這邊也可以看到文件式模型的優勢。

第三點是思想轉換，如果以前用關聯式資料庫用的很習慣，文件式資料庫會少了一些多對多的連結。這在設計應用程式的時候需要考慮，這是我根據實務經驗得出的感想。例如 Firestore 是適用在攜帶型裝置（mobile device）的文件式資料庫。他為了讓不同的裝置、應用程式同步資料，設計成文件式資料庫會讓他好用很多，但也少了關聯式資料庫可以的一些特性。

### 收斂

隨著時間演進，兩個模型相似性其實越來越像：

-   關聯式資料庫支援 JSON 格式的欄位
    -   PostgreSQL
    -   MySQL,
    -   IBM DB2
-   資料式資料庫透過文件參考（document reference）做聯合（join）
    -   RethinkDB
    -   MongoDB 的 driver
-   關聯式資料庫的資料局部性（data locality）
    -   Google Spanner 透過綱目宣告其屬於哪個母表（parent table）來做到局部性
    -   Oracle 的 multi-table index, Bigtable（Cassandra, HBase） 的 column-family 也都類似

## 圖像式模型

前面我們有提到資料的關係會決定使用的模型。

當資料有很多一對多的關係時，文件式模型就很適合。反之，簡單的多對多，關聯式資料庫就可以輕易上手。

但是當資料有大量多對多的關係時，就需要考慮其他的方式。

### 多對多

多對多的關係可被發現於：

-   人際關係
-   網頁關係
-   道路

雖然例子都是同值性資料的應用，但是實際上，每個節點可以不是同值性的資料。例如 Facebook 的圖像式模型會把使用者的事件、位置、打卡、留言等等當成節點，並存成[一張大表](https://www.usenix.org/conference/atc13/technical-sessions/presentation/bronson)。

![多對多關係可以連結完全不同類型的資料](https://github.com/Vonng/ddia/raw/master/img/fig2-5.png)

以書中範例來做講解，節點可以是人或是位置，並非同值性的資料。

這邊也可以注意到因為每個國家對於地區的分界有不同名稱，法國的 _departement_ 和英國的 _country_，雖然在這張表中層級一樣，但是意義可能不一樣。你可以想像如果是做成關聯式資料庫，地區的表就會需要有很多欄位。

再來看線，每個線因為代表著點和點的關係，所以可以有不同意義。

這裡有幾點要注意：

-   任何點和其他任何點都可以連結
-   給定一個點，可以快速找到和其有所連結的點。不管是進還是出。
-   因為線上有標號，所以可以賦予線不同意義

這樣做除了可以保持資料庫結構的乾淨，不需要一直調整綱目外，也賦予圖像式模型很大的彈性，例如：

-   _國家 A_ 被_國家 B_ 併購，變成_城市 A_。原本出生於_國家 A_ 的人，要改成出生於_國家 B_ 下的_城市 A_。如果是關聯式資料庫，因為層級改變了，要調整的東西很多。
-   今天除了要設定國家外，還想要設定使用者喜歡吃的食物，可以不需要調整綱目直接增加節點和線。

我們對圖像式模型有個概念之後，就來看看他有哪些實作。

### 圖像式模型種類

我們會來介紹一下圖像式模型的兩種結構

[屬性圖模型（property graphs model）](#_14)

-   [Neo4j](https://neo4j.com/developer/data-modeling/)
-   Titan
-   InfiniteGraph

[三元組模型（triple-stores model）](#_15)

-   Datomic
-   AllegroGraph

但是這兩種東西其實大同小異，我們待會介紹的時候可能會比較有感。

#### 屬性圖模型

每個點和線會有很多屬性：

-   點：ID、種類、屬性
-   線：ID、起始點、終點、標號（label）、屬性

這樣看可能沒時麼感覺，如果使用關聯式資料庫，可能就會長成這個樣子：

```sql
CREATE TABLE vertices (
    vertex_id   integer PRIMARY KEY,
    vertex_type text,
    properties  json
)
CREATE TABLE edges (
    edge_id     integer PRIMARY KEY,
    tail_vertex integer REFERENCES vertices (vertex_id),
    head_vertex integer REFERENCES vertices (vertex_id),
    label       text,
    properties  json
)
```

以 Neo4j 這個資料庫為例，建立上面的圖像式模型關係網絡需要下以下語法：

```cypher
CREATE
    /* vertices */
    (NAmerica:Location {name:'North America', type:'continent'}),
    (     USA:Location {name:'United States', type:'country'  }),
    (   Idaho:Location {name:'Idaho',         type:'state'    }),
    (    Lucy:Person   {name:'Lucy'}),
    /* edges */
    (Idaho) -[:WITHIN]->  (USA)   -[:WITHIN]-> (NAmerica),
    (Lucy)  -[:BORN_IN]-> (Idaho)
```

值得注意的是，因為圖像式資料庫已經幫你預設好綱目要長的樣子，所以不需要設定，我們直接看添加資料時會要跑的程式碼。

現在若要找「所有從美國移民到歐洲的人的名字」這資料就可以下相關 query：

```cypher
MATCH
    (Person) -[:BORN_IN]->  () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
    (Person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (en:Location {name:'Europe'}),
RETURN Person.name
```

這個聲明式語言讓查詢透過較為高層次的邏輯去執行，我們不必在意實作細節，例如該從人去依序找下去還是從最上層的地區往下找出生於此的人。

除此之外，比較複雜的語法還有「推薦使用者餐廳：有哪個人的朋友有在沒去過的餐廳打卡？」。

#### 三元組模型

和屬性圖模型大同小異，他是以 `(subject,predicate,object)` 方式去建立的。其代表的意義分別是：_主詞_、_術語_、_受詞_。

我們來看看建立時的語法：

```turtle
@prefix : <urn:example:>. (1)
_:lucy      a :Person;   :name "Lucy";          :bornIn _:idaho.
_:idaho     a :Location; :name "Idaho";         :type "state";   :within _:usa
_:usa       a :Loaction; :name "United States"; :type "country"; :within _:namerica.
_:namerica  a :Location; :name "North America"; :type "continent".
```

1. prefix 可以想像成 namespace 的概念。

> 上面的表達格式是 [Turtle](http://www.w3.org/TeamSubmission/turtle/) 格式。

我們來看看使用 SPARQL 搜尋時的語法：

```sparql linenums="1"
PREFIX : <urn:example:>
SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn  / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
```

> SPARQL（sparkle），[可以到高雄市資料平台玩玩看](https://api.kcg.gov.tw/Ontology/Sparql)

由此我們就可以了解圖像式模型概念不難，其實只是因為應用需求的不同，去建立不同的儲存方式。看完了這些模型，我們就來看看查詢語言。

## 查詢語言

查詢語言（query language）這裡介紹三種：

-   [聲明式（Declarative）](#_17)
-   [命令式（Imperative）](#_18)
-   [邏輯式（Deductive）](#_21)

前面在圖像式模型看到很多聲明式查詢語言，他的概念就是把搜尋時的抽象程度拉高，不必讓開發人員去了解或選擇實作方式。

相對而言，還有命令式語言和邏輯式語言，我們下面將以程式碼為範例。

### 聲明式

以 JavaScript 為例，聲明式可能如下：

```javascript
return animals.filter((animal) => animal.family === "Sharks");
```

你不需要考慮怎麼做迴圈，也不需要考慮怎麼收集篩選後的資料，不管他是不是會分散於不同線程等等。

!!! info "對應於 SQL"

    ```sql
    SELECT * FROM animals WHERE family = 'Sharks'
    ```

### 命令式

以 JavaScript 為例，命令式可能如下：

```javascript
function getSharks(animals) {
    var sharks = [];
    for (var i = 0; i < animals.length; i++) {
        if (animals[i].family === "Sharks") {
            sharks.push(animals[i]);
        }
    }
    return sharks;
}
```

你命令程式語言去怎麼跑所有資料，然後也闡明需要以何種方式做結果。

### 聲明式好處

-   高抽象程度，好理解
-   更新底層運作方式而不用改動程式碼，底層運作可能包括
    -   搜尋演算法
    -   並行處理（parallel processing）
    -   等等

### 命令式好處

我們以「海洋生物學家每月觀察到的鯊魚數」來做討論。

```javascript linenums="1"
db.observations.mapReduce(
    // (1)
    function map() {
        var year = this.observationTimestamp.getFullYear();
        var month = this.observationTimestamp.getMonth() + 1;
        emit(year + "-" + month, this.numAnimals);
    },
    // (2)
    function reduce(key, values) {
        return Array.sum(values);
    },
    {
        query: { family: "Sharks" }, // (3)
        out: "monthlySharkReport",
    }
);
```

1. Map 代表從資料庫中每筆（row/document）篩選出多組 k-v 組合，就好像資料結構中的 map 一樣
2. Reduce 代表從 Map 中的 k-v 組合，相同的 key 會被分配到同一組，然後做降冪
3. 聲明式的方式去篩選種類為鯊魚的動物

> 上表是 MongoDB MapReduce 的擴充套件的規則。MapReduce 之後在批次處理會講。

事實上，上述的例子中，是介於命令式和聲明式之間，例如第 11 行就是聲明式的方式去篩選種類為鯊魚的動物。

一開始看，可能會看不太出來命令式的好處。但是：

-   若考慮細緻調整，例如機器學習
-   單純呼叫函式可以很快速的把這個運算分配到多台資料庫中（聲明式一樣可以做到，但是會很不直觀，例如 MPP）

### 邏輯式

Prolog（Programming in Logic）就是透過邏輯的方式去寫程式碼。不像其他類型的語言比較像是命令式的方式去撰寫。然而，早在 1970 年代邏輯式的語言就已經發展了。早期在研究時，這種邏輯式的語言相對於命令式更容易讓人理解。

我們以 Prolog 的一個使用情境「發生一場命案，請透過互斥的證詞找出誰在說謊」為例：

-   A: B 是 受害者（V） 的朋友，且 C 和 V 互相討厭。
-   B: 事情發生時我不在現場，而且我不認識 V。
-   C: 我是無辜的，但事發時，我看到 A 和 B 在現場，可是我不知道究竟誰做的。

上述狀況可以透過下面的語法成功找到誰在說謊：

```prolog linenums="1"
% 定義證詞
testimony(a, friend(b)). % (1)
testimony(a, enemy(c)).
testimony(b, out_of_town(b)).
testimony(b, stranger(b)).
testimony(c, in_town(c)).
testimony(c, in_town(a)).
testimony(c, in_town(b)).

% 宣告什麼是衝突的
inconsistent(friend(X), enemy(X)).
inconsistent(friend(X), stranger(X)).
inconsistent(enemy(X), stranger(X)).
inconsistent(out_of_town(X), in_town(X)).

% 找出說謊者
lier(L) :-
 member(L, [a, b, c]),          % 從 a, b, c 中拉出一個人叫 L(lier)
 select(L, [a, b, c], Witness), % 剩下的人算進證人
 consistent(Witness).           % 證人的證詞是合理的

% 群組中大家證詞都是合理的
consistent(W) :-
 \+ inconsistent_testimony(W).

% 群組中有人有衝突的證詞
inconsistent_testimony(W) :-
 member(X, W),          % 從群組中挑出 X 和 Y
 member(Y, W),
 X \= Y,                % X 和 Y 不同人
 testimony(X, XT),      % 拿出 X 的其中一個證詞
 testimony(Y, YT),      % 拿出 Y 的其中一個證詞
 inconsistent(XT, YT).  % 他們是衝突的
```

1. 這裡的定義證詞，根據每個人的邏輯不同，可能有不同寫法。例如：

    ```text
    testimony(a, knew(b)).
    testimony(a, knew(c)).
    testimony(a, innocent(a)).
    testimony(b, out_of_town(b)).
    testimony(b, stranger(b)).
    testimony(c, innocent(c)).
    testimony(c, in_town(a)).
    testimony(c, in_town(b)).
    ```

相對於常見的命令式語言，通常很難做出這類的表現，因為我們會把邏輯放在腦中，並把實作寫成語言。其概念和邏輯式語言正相反。

**Datalog**

Datalog 是 Prolog（Programming in Logic）下的集合。就像 SQL 是一種規範一樣，Datalog 也是一種軌範，有不同的搜尋語言去實踐它。例如 `Cascalog`。

```datalog
within_recursive(Location, Name) :- name(Location, Name). /* (1) */

within_recursive(Location, Name) :- within(Location, BiggerLoc),
                                    within_recursive(BiggerLoc, Name).

migrated(Name, BornIn, LivingIn) :- name(Person, Name),
                                    born_in(Person, BornLoc),
                                    within_recursive(BornLoc, BornIn),
                                    lives_in(Person, LivingLoc),
                                    within_recursive(LivingLoc, LivingIn).

?- migrated(Who, 'United States', 'Europe').
/* Who = 'Lucy'. */
```

1. Fallback function，當資料沒有 `within` 就取名稱。

> Datalog 宣告沒有順序，和 Prolog 相反。

---

## 總結

![各查詢語言和模型的總結](https://i.imgur.com/gjVmHj4.png)

這章討論了一些模型，但是並未深入探討其內部運作方式。事實上，要深入了解一個模型是需要大量時間和精神的，但是對於不同模型有些初步和概念性的了解，可以幫助你在選擇時加入一些參考。

下一章我們將討論實作資料庫時，需要考慮的不同取捨。

---

補充：

-   其他模型
    -   科學上使用，需要儲存大量狀態的資料庫。例如，強中子對撞機的 [ROOT](https://root.cern/)
    -   基因資料庫，長字串的相似性。例如，[GenBank](https://www.ncbi.nlm.nih.gov/genbank/)
    -   文本搜尋。例如，Elasticsearch
-   圖像式模型和上面提的 CODASYL 看起來好像都要循線去找到某個點，但是有些差異：
    -   圖像式模型的綱目很單純，任何點都可以和其他任何點連結
    -   圖像式模型的線是沒有順序性的，CODASYL 在考慮儲存時的狀況，一對多關係是有順序性的
    -   CODASYL 是命令式的搜尋語言，大部分圖像式模型的搜尋語言式聲明式的
-   語意網站（semantic web）和三元組模型很像，但是卻是兩個意義不同而實作方式相似的東西。

--8<-- "abbreviations/ddia.md"
