# 編碼和進程

應用程式無可避免地需要演進，在改變應用程式的同時，通常也會需要調整資料的結構。如何讓應用程式在使用資料時保持前後相容？

資料在做儲存或輸出的時候是需要編碼（encoding）的，除了可以幫助壓縮資料量、加速效能外，
好的編碼方式也能提供良好的前後相容。

HackMD [報告文本](https://hackmd.io/@Lu-Shueh-Chou/HkZhtqciK)

## 編碼

當你把資料存進記憶體中，可以透過各種資料型別去對資料進行操作，例如陣列、物件等等。然而當把資料存進磁碟（filesystem）中或者透過網路傳送給其他服務時，就需要以編碼後的資料（例如 JSON 格式）來儲存或輸出。

### 程式碼內建

我們都會透過程式語言來和記憶體溝通，不同程式語言預設就有些編碼方式，Java：`java.io.Serializable`、Ruby：`Marshal`、Python：`pickle`，然而

- 通常不同語言之間是無法互相接通的
- 可能會觸發物件的建置，有安全性疑慮
- 並非以「前後相容」為設計核心
- 效率通常很差

### 方便人類閱讀

JSON、XML、CSV，這些格式都很常見，不需要綱目就能解碼。然而

- 佔空間
  - 無法儲存二進位文字，雖然可以使用 Base64 把二進位轉換成 Unicode 文字，卻需要額外的效能和體積
  - Base64 每 6 個 bit 轉成一個 ASCII 字元（1 個 byte），所以體積會比直接做二進位轉換大 1.3 倍
- 沒有綱目，花時間理解和管理
- 大數字不好儲存，整數、小數的區分

然而這些仍是主要的編碼方式，也因為大家很習慣這些方式的編碼，導致更有效和更方便管理的編碼方式很難吸引到大家的目光。

### 二進位 JSON

有些格式是以 JSON 為基礎做演化的，其嘗試解決上述問題，但是效率仍無法贏過專門的二進位編碼，以 MessagePack 為範例：

原始 JSON 資料：

```json
{
    "userName": "Martin",
    "favoriteNumber": 1337,
    "interests": ["daydreaming", "hacking"]
}
```

![MessagePack 編碼範例](https://github.com/Vonng/ddia/raw/master/img/fig4-1.png)

我們可以得到 66 Bytes 的資料，確實比原本 88 Bytes 好，但是和待會我們可以看到減少到 32 Bytes 的方式仍有差異。

> 由於他是延伸 JSON，天生上仍然沒有綱目，所以每個物件仍然需要儲存鍵的資料（例如：`userName`）。

### 二進位編碼

二進位編碼並不是新東西，早在 1984 年就有協定 [ASN.1](https://www.oss.com/asn1/resources/books-whitepapers-pubs/larmouth-asn1-book.pdf) 闡述如何進行二進位編碼，他和 [Thrift](#thrift)、[Protocol Buffer](#protocol-buffer) 一樣都使用 tag ID。且其應用（DER）如今仍被大量使用於 X.509。

但是他卻過於複雜且其文件也設計得很複雜，由此發展出以下幾個較新的方式。

- [Apache Thrift] - 初始於 Facebook
- [Protocol Buffer] - Google
- [Apache Avro]

上述方式可以降低磁碟的使用量、高效能編（解）碼、有效製作文件檔，但缺點就是需要解碼才能讓人類讀懂訊息。

> 在資料準備要送到資料儲倉（warehouse）時，也需要編碼，這時候可以把資料轉換成友善於行式資料庫（column-oriented database）的格式，例如 [Parquet](https://parquet.apache.org)。

### 前後相容

在做編碼時都需要去考慮前後相容：

- 向後相容：舊的程式碼讀到的資料含有新的綱目定義的欄位時，仍然可以運行
- 向前相容：新的程式碼讀到的資料含有已經被刪除或不同格式的欄位時，仍然可以運行

由此可知，JSON 這類編碼方式新舊版本都可以做解碼，只要在程式邏輯上注意一下就可以保持前後相容。

### 程式碼產生器

在使用需要編譯的語言（Java、C++）時，可以利用綱目去產生相應物件的程式碼（code generation），幫助編譯時的型別判定。例如關於「人」的綱目，就可以根據綱目建立對應的物件，並且產生對應的 property，例如姓名（`var person = new Person(object);print(person.name);`）。但是在根據資料動態調整綱目的狀況時，這樣的機制在設計時就很麻煩。

> 相對而言腳本型的語言（JavaScript、Python、Ruby、PHP），不需要產生程式碼來幫助編譯

!!! note

    雖然 JSON 可以用額外工具設定綱目，但是他把編解碼和綱目管理當成兩件事：編碼時不需要考慮綱目一樣可以做
    相反，二進位編碼是和綱目同生的，沒有綱目就無法編碼

## 二進位編碼的比較

以下就 [Apache Thrift]、[Protocol Buffer] 和 [Apache Avro] 來做二進位編碼的比較。

### Apache Thrift

[Apache Thrift] 會使用綱目：

```IDL
struct Person {
  1: required string       userName,
  2: optional i64          favoriteNumber,
  3: optional list<string> interests
}
```

並有兩種方式做編碼，**BinaryProtocol** 和 **CompactProtocol**，依序方式為：

- BinaryProtocol
    ![Apache Thrift BinaryProtocol，會得到 59 Bytes](https://github.com/Vonng/ddia/raw/master/img/fig4-2.png)
- CompactProtocol
    ![Apache Thrift CompactProtocol，會得到 34 Bytes](https://github.com/Vonng/ddia/raw/master/img/fig4-3.png)

### Protocol Buffer

[Protocol Buffer] 的綱目如下：

```IDL
message Person {
  required string user_name       = 1;
  optional int64  favorite_number = 2;
  repeated string interests       = 3;
}
```

![Protocol Buffer，會得到 33 Bytes](https://github.com/Vonng/ddia/raw/master/img/fig4-4.png)

### 註

- `required` 和 `optional` 在編碼時，不影響結果，僅會在做解碼時 runtime 輸出錯誤。
- 每個 tag ID 不去更動來保持前後相容。當使用舊的綱目去讀取未知欄位時，省略之。
- 新增欄位時若設定 `required` 會讓舊程式碼輸出錯誤，需要給定預設值。
- 變更檔案格式可能導致資料不完全，例如 `int8` 轉到 `int16`
- _ProtocolBuffers_ 沒有 `list` 資料型態，讓他很好從 `repeated` 轉到 `optional`，但巢狀結構就會需要額外功來達成。

### Apache Avro

[Apache Avro] 的綱目：

```IDL
record Person {
  string               userName;
  union { null, long } favoriteNumber = null;
  array<string>        interests;
}
```

> Avro 是作者有貢獻的開源編碼方式

這裡多了一個 union，除了明確標示哪些是 nullable 之外，就不需要 required/optional 了。

![Apache Avro，會得到 32 Bytes](https://github.com/Vonng/ddia/raw/master/img/fig4-5.png)

在解碼時，資料一的型別和名稱就是綱目上第一組資料所展示的型別。
由於在編碼後，沒有型別和 ID，所以必須有對應的綱目才能解碼。

#### 細節

Apache Avro 並沒有使用 tag ID 來辨認每個資料的位置，而是透過綱目不同版本間的轉換：

![編解碼時，會有機制對應不同版本的綱目](https://github.com/Vonng/ddia/raw/master/img/fig4-6.png)

因此讀取資料時，需要先確保撰寫資料所使用的綱目版本。

Apache Avro 也利用 `union { null, int }` 來當作資料的 _required/optional_，同時給予預設值來滿足向後（前）相容。

除此之外，Apache Avro 還允許更改資料的**型別**和**名稱**：

- **型別**和上面提的對應機制很像，在程式實作需要設計型別的轉換。
- 設定 `alias` 來滿足名稱的轉換，但只能滿足向後相容（舊綱目看不懂新綱目調整名稱後的資料）

#### 如何知道編碼時的綱目版本

根據應用程式而有差異：

- 若資料庫是在 Hadoop 架構之上，就可以在每份檔案前面添加綱目版本。
- 若資料庫的每筆資料都可能會有不同的版本，就需要在每筆資料前設定版本，如 [Espresso](https://dbdb.io/db/espresso)。
- 若是在網路上進行雙向溝通的應用程式，可以協商出彼此的版本，如 [Avro RPC](https://avro.apache.org/docs/current/spec.html#Protocol+Declaration)

> 把所有版本的綱目都存進 DB 可以幫助未來檢查和備份。

#### 不需要使用 tag ID 有什麼好處

資料輸出成檔案時（Hadoop 架構下的資料庫常做的事），我可以很方便地從資料庫的綱目轉換成 Avro 的綱目，然後把檔案撰寫成二位元。同樣的，當資料庫的綱目更新時，我們再產生新的綱目，由於是對應欄位名稱，就不會有衝突了。例如，新增一個欄位叫 countryId 並同時移除欄位 countryName，再依此資料庫綱目產生 Avro 綱目時，可以順利的用舊（新）綱目讀新（舊）資料。

相反的，用 Protocol Buffers 或 Thrift 就需要謹慎使用 tag ID 來避免任何衝突。以上述例子為例，就會出現相同 tag ID 卻是不同欄位的狀況（例如，countryId 和 countryName 都是 tag 5）。

> Protocol Buffers、Thrift 是為了 RPC 這類操作而設計的編碼格式

#### 自描述

如果在資料中有放置編碼時的綱目，我們稱為其能夠自描述（self-describing）。若資料能夠自描述，你可以直接透過對應編碼方式的程式庫（例如 Avro library）打開這份檔案，不需要額外再提供綱目。同時，又保證資料不會過大。

這對於高維度的分析工具，如 [Apache Pig](https://github.com/apache/pig)，很有幫助。使用者直接透過 SQL 語法在 Hadoop 架構之上的資料庫進行分析，並且產出新的資料，過程中都不需要考慮綱目的問題，因為 Avro 會在資料的前面定義綱目。

### 複習差異

Schema-less 編碼（JSON）有其優點：

- 在解碼時不會受綱目影響，可輕易（資料庫面）允許向後（前）的相容。
- 可以透過文件方式補足綱目，且能詳細限制資料。如：數字只能在 0~1 之間。

然而二進位編碼也有其好處：

- 儲存更緊密，體積小。
- 因為綱目（Schema）是必須的，不會出現文件和實際運作有落差（忘記補文件）。
- 在 compile 過程就能檢查程式碼是否符合綱目。
- 透過一些機制仍能保持向前（後）的相容讓他和 Schema-less 的編碼一樣好用

## 編（解）碼的使用情境

我們已經理解編碼是可以透過其內部機制，去讓使用該編碼方式的人可以不需要考慮怎麼相容不同版本的綱目，接下來透過實際使用場景來感受一下其應用。

- 透過資料庫
- 兩個服務或使用者彼此溝通
- 異步訊息傳遞（Asynchronous message passing）

### 透過資料庫

應用程式把資料傳給資料庫，並預期未來要可以拿到指定的資料。

- 編碼：傳遞資料時；資料庫寫進磁碟時
- 解碼：接收傳到的資料時；資料庫讀磁碟的資料時

必須向後相容（新綱目讀舊資料），因為是傳給其他人（寫進磁碟）後，未來的自己使用新綱目做讀取。

> 除非你每次更動綱目都要把資料庫所有資料重新編碼一次，否則更動綱目理論上舊資料在編碼上仍是以舊的綱目為準。
> MySQL 就是那個例外。

當其他服務傳送資料給資料庫時，其以為的綱目很可能是舊的，這時也需要向前相容，這時就要避免資料被舊程式碼覆蓋掉：

![剛木相容性](https://github.com/Vonng/ddia/raw/master/img/fig4-7.png)

還有個狀況需要注意：當資料庫要把資料做備份或輸出給 [_資料倉儲_](foundation-dw.md) 時，也會需要一次性把大資料重新編碼（做 ETL）。資料庫內部可能會有多個版本的綱目去做編碼的資料，而這些資料既然都要匯出去，那就重新編碼進最新版本。

### 兩個服務彼此溝通

可能是服務間（不管是不是相同公司）的溝通，也可能是使用者（例如瀏覽器、手機 APP）和服務間的溝通

- 請求者把請求資訊編碼
- 服務者解碼
- 服務者把回應編碼
- 請求者解碼

暴露接口（API）的 REST/GraphQL，還有依照規範，在程式碼中包裝起來的 RPC/SOAP。

比較：

- RPC/SOAP 被函式庫包裝後，就像呼叫函示一樣，可以直接呼叫。反之，REST/GraphQL 就需要參閱提供者的文件。
- RPC/SOAP 無法保證 client 使用最新版本的 Schema，所以較難維運。反之，RESTful API 可以利用：
  - 前綴詞加上版本
  - HTTP 標頭（_Accept_）寫明使用版本
  - 請求時需攜帶 Token
- RPC/SOAP 通常會使用較有效率和適合前後相容的編碼方式

總結來說，RPC/SOAP 適合同公司不同服務間的呼叫，快速且前後相容。反之 REST/GraphQL 適合對外，不管是使用者（瀏覽器、APP）和服務間的溝通或者不同公司間的服務溝通。

!!! info

    以下是不同編碼方式在 RPC 之上的一些實作：

    - Protocol Buffers - Google [gRPC](https://github.com/grpc)
      - 之前有撰寫過[心得](../distributed-systems-with-node.js/protocol.md)
    - Thrift - Twitter [Finagle](https://github.com/twitter/finagle)
    - JSON - LinkedIn [Rest.li](http://github.com/linkedin/rest.li/)

### 非同步訊息傳遞

這塊較不熟悉，因此另外搜集資料。非同步訊息和同步訊息的差異在於

- 同步訊息預期收到請求，例如 REST API。這代表當沒收到請求時，需要做錯誤處理（Error handling）
- 非同步訊息則相反，送出訊息後，在確認對方收到前（根據設定可能不需要確認）可能又再送出一則訊息

非同步訊息傳遞書中主要介紹兩種方式：

- 消息代理（Message brokers）
  - 事件串流式架構（Event streaming platforms）
  - 企業服務匯流排（Enterprise service bus）
- 分散式演員模型（Distributed actor model）

> 此種方式，介於第一二種中間。
> 第一種透過資料庫，應用程式完全讓資料庫處理編碼；
> 第二種應用程式和使用者（可能是其他應用程式或瀏覽器等等），則是彼此協商出一起用的編碼方式。

相對來說，非同步訊息傳遞則是大家預設使用某種編碼，但是傳遞是透過第三方。

#### 消息代理

透過一個代理人，幫我把訊息傳遞給其他有興趣的接收者。故而我只要確保資料送給代理人即可，其他接收者是否有收到是代理人要做的事情。

![消息代理說明](https://i.imgur.com/3kWs9j1.png)

> [Message Broker Pattern using C#](https://www.codeproject.com/Tips/1169118/Message-Broker-Pattern-using-Csharp)

和代理人間的溝通其編碼方式和直接兩個服務溝通很像，因為代理人不會在乎你使用什麼編碼方式，
他只是進行訊息的傳遞而已。但有時接收者會把訊息消化並重新傳給代理人
（再讓其他有興趣的人接受其輸出），此時就有可能發生[上述提到的](#透過資料庫)覆蓋資料的問題。

> 這段到[串流處理](derived-stream.md)會更詳細的討論，這邊僅說明其會使用到編碼。

##### 事件串流式架構

其和消息代理很類似，但是僅提供多對一（pub/sub）的服務並且較適合處理大量訊息。

![事件串流式架構說明](https://cdn.confluent.io/wp-content/uploads/2016/08/slide-15e.png)

> [Making sense of stream processing](https://www.confluent.io/blog/making-sense-of-stream-processing/)

事件架構對於資料傳遞和整個組織的資料整合來說非常好用，會在第十一章的時候詳細提。

##### 企業服務匯流排

企業服務匯流排為較大型的消息代理者，處理多對多的溝通，會負責把傳遞中的訊息格式統一。
例如 XML 轉成 JSON。

![企業服務匯流排](https://i.imgur.com/t2uMqR8.png)

> [WIKI](https://zh.wikipedia.org/wiki/企业服务总线)

但是[慢慢式微](https://www.ibm.com/cloud/learn/message-brokers#toc-message-br-oBdNX5GN)，因為會越搞越複雜。

#### 分散式演員模型

演員模型是一種程式設計的哲學，其主旨是獨立每個運行的邏輯和其狀態，並把這獨立的單位稱為演員（Actor）。

例如現在有個演員會負責輸出「Hello World」，我們傳遞一個訊息給這個演員，
告訴他我這裡有個變數 3，作出任何你應該要做的事情吧。
然後這個演員就會開始輸出「Hello World」三次。

演員模型的價值在於它預設各演員很可能發生錯誤，且彼此之間沒有共用任何資源。
所以其應用不只局限於程式碼之間的訊息傳遞，你一樣可以通過網際網路的方式傳遞，
就好像 API 一樣（類似 RPC 想做的事）。

??? example "以 Akka 為例"

    以 Java 的演員模型框架 [Akka](https://github.com/akka/akka) 為例：

    ```java
    public class HelloWorld extends AbstractBehavior<HelloWorld.Command> {

    interface Command {}

    public enum SayHello implements Command {
        INSTANCE
    }

    public static class ChangeMessage implements Command {
        public final String newMessage;

        public ChangeMessage(String newMessage) {
        this.newMessage = newMessage;
        }
    }

    public static Behavior<Command> create() {
        return Behavior.setup(context -> new HelloWorld(context));
    }

    private String message = "Hello World";

    private HelloWorld(ActorContext<Command> context) {
        super(context);
    }

    @Override
    public Receive<Command> createReceive() {
        return newReceiveBuilder()
        .onMessageEquals(SayHello.INSTANCE, this::onSayHello)
        .onMessage(ChangeMessage.class,this::onMessageChange)
        .build();
    }

    private Behavior<Command> onSayHello() {
        System.out.println(message);
        return this;
    }

    private Behavior<Command> onMessageChange(ChangeMessage command) {
        message = command.newMessage;
        return this;
    }
    }
    ```

    上述演員在收到 `SayHello.INSTANCE` 就會執行 `onSayHello`，收到 `ChangeMessage` 這一類別的訊息時會執行 `onMessageChange`。

    準備好演員，就可以開始執行劇場工作囉：

    ```java
    ActorSystem<HelloWorld.Command> mySystem = ActorSystem.create(HelloWorld.create(), "MySystem");

    // 告訴演員 `HelloWorld.SayHello.INSTANCE` 這則訊息
    mySystem.tell(HelloWorld.SayHello.INSTANCE);
    mySystem.tell(HelloWorld.SayHello.INSTANCE);
    // 告訴演員 `HelloWorld.ChangeMessage` 這個型別的訊息
    mySystem.tell(new HelloWorld.ChangeMessage("Hello Actor World!!"));
    mySystem.tell(HelloWorld.SayHello.INSTANCE);
    mySystem.tell(HelloWorld.SayHello.INSTANCE);
    // 最後輸出：
    // Hello World
    // Hello World
    // Hello Actor World!!
    // Hello Actor World!!
    ```

    [Referrer](https://youtu.be/rIFqJxMJ1MM)

---

[apache thrift]: http://thrift.apache.org
[protocol buffer]: https://developers.google.com/protocol-buffers
[apache avro]: http://avro.apache.org

--8<-- "abbreviations/ddia.md"
